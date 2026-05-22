# Expected Output Outline

A good answer should include:

1. **Data Coverage And Harvest Gate**
   - State connection mode, windows, available reports, missing purchased-product data, missing full margin, duplicate-risk, current negative checks, destination feasibility, and whether harvest actions are action-safe.

2. **Rocketcart Live Context**
   - In standalone mode, state that Rocketcart MCP was not used.
   - In Rocketcart MCP mode, state profile, live reads used, exact ID resolution, recent drift/snapshots checked, product context checked, and live limitations.

3. **Executive Summary**
   - Identify top harvest-ready terms, controlled tests, blocked/duplicate terms, and negative-risk warnings.

4. **Search Term Classification Table**
   - Classify each meaningful term with source, traffic type, lifecycle stage, orders, spend, sales, ACoS/CPA, relevance, destination, confidence, primary outcome, and write-readiness status.

5. **Harvest Action Rows**
   - Include mode, source campaign/ad group IDs, search term, destination campaign/ad group IDs, match type, current state, current value, proposed value, bid direction, source negative decision, duplicate check, current negative check, live resolution status, live preflight status, destination feasibility, reason, risk, confidence, approval status, execution status, approval text, preflight, readback, monitoring, and write-readiness status.

6. **Negative And Routing Decisions**
   - Add source negatives only when safe routing or waste evidence supports them.
   - Block negatives for brand defense, own-ASIN defense, launch/rank-defense, profitable discovery, or unclear relevance.

7. **Blocked / Watchlist Terms**
   - Use watchlist for low sample, unclear destination, missing data, duplicate-risk, or retail-readiness blockers.

8. **Execution Gate**
   - State that no rows were executed during live review.
   - For explicit execute requests, require exact row approval, live preflight, matching current values, readback, and monitoring.

9. **Monitoring Plan**
   - Include 3-day delivery checks, 7-day spend/order checks, 14-day ACoS/CVR/route-quality checks, and failure responses.

10. **Missing Data / Next Pulls**
   - Prioritize purchased-product report, exact keyword/negative map, margin, organic rank, competitor context, live IDs, live negatives, snapshots, and product context.
