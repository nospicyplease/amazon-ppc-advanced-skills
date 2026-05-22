# Expected Behavior

The reviewer should fail the output.

An ASIN-like query needs ASIN relationship context before product-target expansion or source negatives. It may be own-ASIN defense, substitute, complement, or irrelevant traffic. A good answer should classify as `Product Target Candidate / Own-ASIN Defense Check` with `NEEDS_DATA`.
