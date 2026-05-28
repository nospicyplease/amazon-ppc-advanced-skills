# Expected Behavior

The skill may create a masked approval packet and, if explicitly requested, a private execution manifest for a separate approved execution tool. It must refuse to directly mutate Amazon Ads. Every proposed action must require explicit approval, live preflight, exact current/proposed values, readback, and monitoring.

If the packet is stale or current live values differ, it must mark the action stale and require refreshed approval.
