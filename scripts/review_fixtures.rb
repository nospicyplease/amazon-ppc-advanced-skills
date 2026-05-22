#!/usr/bin/env ruby
# frozen_string_literal: true

require "pathname"

ROOT = Pathname.new(__dir__).parent.expand_path

def fail_with(message)
  warn "review-fixtures: #{message}"
  exit 1
end

def read(path)
  Pathname.new(path).read
rescue Errno::ENOENT
  fail_with("missing required file: #{path}")
end

def make_list(var)
  makefile = read(ROOT / "Makefile")
  match = makefile.match(/^#{Regexp.escape(var)}\s*:=\s*(.+)$/)
  fail_with("Makefile is missing #{var}") unless match

  match[1].split(/\s+/).reject(&:empty?)
end

def assert_file(path)
  fail_with("missing required file: #{path.relative_path_from(ROOT)}") unless path.file?
  fail_with("empty required file: #{path.relative_path_from(ROOT)}") if path.read.strip.empty?
end

def assert_dir_with_files(path)
  fail_with("missing required directory: #{path.relative_path_from(ROOT)}") unless path.directory?
  files = path.children.select(&:file?)
  fail_with("directory has no files: #{path.relative_path_from(ROOT)}") if files.empty?
end

def section_body(text, heading)
  match = text.match(/^## #{Regexp.escape(heading)}\s*$([\s\S]*?)(?=^## |\z)/)
  match && match[1].strip
end

def review_examples(skills)
  required = %w[
    prompt.md
    input-summary.md
    expected-output-outline.md
    expected-output.md
    known-bad-output.md
    eval-result.md
  ]

  skills.each do |skill|
    dir = ROOT / "examples" / skill
    fail_with("missing example pack for #{skill}") unless dir.directory?

    required.each { |file| assert_file(dir / file) }
    assert_dir_with_files(dir / "sample-data")
  end

  example_dirs = (ROOT / "examples").children.select(&:directory?).map { |p| p.basename.to_s }.sort
  extras = example_dirs - skills
  fail_with("example directories not listed in SKILLS: #{extras.join(", ")}") unless extras.empty?
end

def review_eval_cases(eval_cases)
  case_root = ROOT / "evals" / "cases"
  dirs = case_root.children.select(&:directory?).map { |p| p.basename.to_s }.sort

  missing_from_make = dirs - eval_cases
  missing_dirs = eval_cases - dirs
  fail_with("eval case directories not listed in EVAL_CASES: #{missing_from_make.join(", ")}") unless missing_from_make.empty?
  fail_with("EVAL_CASES entries missing directories: #{missing_dirs.join(", ")}") unless missing_dirs.empty?

  dirs.each do |case_name|
    dir = case_root / case_name
    assert_file(dir / "prompt.md")
    assert_file(dir / "expected-behavior.md")
    assert_file(dir / "rubric.md")

    rubric = read(dir / "rubric.md")
    fail_with("#{case_name}/rubric.md missing Pass Criteria") unless rubric.include?("Pass Criteria")
    fail_with("#{case_name}/rubric.md missing Fail Criteria") unless rubric.include?("Fail Criteria")
  end
end

def review_stress_tests(skills)
  stress_root = ROOT / "stress-tests"
  files = stress_root.children
                     .select { |path| path.file? && path.extname == ".md" && path.basename.to_s != "README.md" }
                     .sort_by { |path| path.basename.to_s }

  fail_with("stress-tests has no stress test files") if files.empty?

  files.each do |path|
    text = read(path)
    rel = path.relative_path_from(ROOT)

    %w[Target\ Skills Prompt Expected\ Resistance Eval\ Prompts\ To\ Use].each do |heading|
      title = heading.tr("\\", "")
      body = section_body(text, title)
      fail_with("#{rel} missing ## #{title}") unless body
      fail_with("#{rel} has empty ## #{title}") if body.empty?
    end

    target_body = section_body(text, "Target Skills")
    unless skills.any? { |skill| target_body.include?("`#{skill}`") }
      fail_with("#{rel} does not reference a production skill from Makefile SKILLS")
    end

    eval_body = section_body(text, "Eval Prompts To Use")
    unless eval_body.scan(%r{evals/[^`\s)]+\.md}).any?
      fail_with("#{rel} does not list any eval prompt paths")
    end
  end

  readme = read(stress_root / "README.md")
  files.each do |path|
    name = path.basename.to_s
    fail_with("stress-tests/README.md does not list #{name}") unless readme.include?(name)
  end
end

def review_unsafe_wording
  unsafe = /
    execute\s+immediately|
    immediately\s+(increase|decrease|lower|raise|pause|add|create|execute)|
    just\s+do\s+it|
    no\s+approval|
    without\s+approval|
    do\s+not\s+ask\s+me\s+for\s+approval|
    execute\s+all|
    write\s+capabilities\s+are\s+available|
    validation\s+was\s+fine
  /ix

  safety = /
    approval|
    approval-gated|
    blocked|
    not\s+executable|
    do\s+not\s+execute|
    refuse|
    expected\s+resistance|
    needs\s+ids|
    preflight|
    readback|
    monitoring|
    fail
  /ix

  roots = [ROOT / "examples", ROOT / "stress-tests"]
  files = roots.flat_map { |root| root.glob("**/*.md") }.reject { |path| path.basename.to_s == "README.md" }

  files.each do |path|
    text = read(path)
    next unless text.match?(unsafe)
    next if text.match?(safety)

    fail_with("#{path.relative_path_from(ROOT)} contains unsafe write language without blocked or approval-gated expected behavior")
  end
end

skills = make_list("SKILLS")
eval_cases = make_list("EVAL_CASES")

review_examples(skills)
review_eval_cases(eval_cases)
review_stress_tests(skills)
review_unsafe_wording

puts "Fixture review passed."
