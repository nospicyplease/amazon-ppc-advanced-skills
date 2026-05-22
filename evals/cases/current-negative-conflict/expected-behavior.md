# Expected Behavior

The reviewer should fail the output.

A destination negative conflict blocks delivery. A good answer should classify the row as `BLOCKED`, require negative review/removal as a separate approval-gated action, and not mark the harvest approval-ready until the conflict is resolved.
