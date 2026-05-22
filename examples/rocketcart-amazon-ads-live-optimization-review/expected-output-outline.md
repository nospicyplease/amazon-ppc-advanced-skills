# Expected Output Outline

A good answer should include:

1. **Mode, Scope, And Data Trust**
   - State `Rocketcart MCP` mode if live tools are used.
   - Confirm profile, marketplace, ad type, live reads, snapshots reviewed, and missing data.

2. **Executive Verdict**
   - Summarize what to protect, what to investigate, what might be action-ready, and whether execution is safe.

3. **Live State And Change Review**
   - Include campaign states, budgets, placement modifiers, budget changes, live drift since snapshot, and snapshot/changelog context.

4. **Read-Only Findings**
   - Separate findings that need no execution from write candidates.

5. **Proposed Action Rows**
   - Include Entity Type, Entity ID, Name, Current State, Proposed Action, Reason, Expected Impact, Risk, Confidence, Preflight, and Approval.

6. **Execution Gate**
   - State that no writes were executed.
   - Mark actions as `Approval Required`, `Preflight Required`, `Needs IDs`, `Needs Data`, or `Monitor Only`.

7. **Readback And Monitoring Plan**
   - Define readback checks after any future approved execution.
   - Include 3-day, 7-day, and 14-day monitoring windows.

8. **Missing Data / Next Reads**
   - Prioritize search terms, BSR, total sales, competitor context, and final approval rows.
