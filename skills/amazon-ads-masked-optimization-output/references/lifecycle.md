# Lifecycle Reference

1. Read source data privately.
2. Validate data coverage and exact metric fields.
3. Analyze using raw IDs.
4. Produce source-plane recommendations.
5. Resolve masked handles for display.
6. Build masked approval packet.
7. Optionally write private execution manifest under an ignored private path.
8. Scan public output.
9. If a separate execution tool runs after explicit approval, activate planned handles only from readback.
10. Produce masked readback and monitoring output.

Never skip from recommendation to mutation inside this skill.
