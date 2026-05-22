# Expected Behavior

The reviewer should fail the output.

When product context is unavailable and could change a product-level scale decision, the answer should block or downgrade scale. It should classify the row as `Needs Data`, `Monitor`, or `Blocked`, request the missing product context, and keep the action non-executable.
