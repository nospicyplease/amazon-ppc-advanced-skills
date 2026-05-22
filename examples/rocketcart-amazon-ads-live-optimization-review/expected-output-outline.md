# Expected Output Outline

A good answer should include:

1. **Mode, Scope, And Data Coverage**
   - State `Rocketcart MCP` mode if live capabilities are used.
   - Confirm profile, marketplace, ad type, live reads, snapshots reviewed, and missing data.

2. **Executive Verdict**
   - Summarize what to protect, what to investigate, what might be action-ready, and whether execution is safe.

3. **Live State And Change Review**
   - Include campaign states, product ads/ASIN mapping, budgets, placement modifiers, budget changes, targeting or negative drift, live drift since snapshot, and snapshot/changelog context.

4. **Product Intelligence And Readiness**
   - Include category/BSR movement, product context, inventory or availability, Featured Offer / Buy Box, price, rating/reviews, estimated demand, competitor signals, BSR responsiveness, ASIN-level controls, and missing product context where available.

5. **Read-Only Findings**
   - Separate findings that need no execution from write candidates.

6. **Proposed Action Rows**
   - Include Entity Type, Entity ID, ASIN/SKU, Name, Current State, Proposed Action, Product Context, Reason, Expected Impact, Risk, Confidence, Preflight, and Approval.

7. **Execution Gate**
   - State that no writes were executed.
   - Mark actions as `Approval Required`, `Preflight Required`, `Needs IDs`, `Needs Data`, or `Monitor Only`.

8. **Readback And Monitoring Plan**
   - Define readback checks after any future approved execution.
   - Include 3-day, 7-day, and 14-day monitoring windows.

9. **Missing Data / Next Reads**
   - Prioritize search terms, full BSR history, total sales, competitor context, ASIN/product-readiness reads, and final approval rows.
