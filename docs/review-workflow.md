# Free-tool review and model interchange

Run the offline tool and inspect `episodes/episode-NNN.json`. Give a permitted AI tool the candidates and `scout.PROMPT`, preferably one episode at a time. Include complete clip dialogue plus the opening/ending action evidence. Ask it to reject poor candidates, not force a choice. If it proposes a different cut, verify that it corresponds to an enumerated candidate from `candidates(ep)`; never accept generated timestamps directly.

For each episode, return an entry with `episode`, `selections`, and an optional rejection rationale. Each selection contains `candidate_id`, integer `hook`, `cliffhanger`, `standalone` (0–5), `why`, and `risk`. Optional `hook_event_id` and `cliffhanger_event_id` must exist inside the clip. At most three selections per episode. An empty list is an explicit abstention.

Wrap all episode entries in a JSON object with `method` (an honest description of who reviewed what), `source_hashes` (episode number string to SHA-256 from the manifest), `coverage` (the manifest coverage array), and `episodes`. Run `review.py` to reject stale source hashes, nonexistent IDs, duplicates, or invalid score types. Do not modify hashes to bypass a stale-input error.

The supplied audit is intentionally limited: one leading baseline candidate per episode, plus four source-assisted recuts. It is not an exhaustive semantic assessment of 26,989 windows. Rejected entries mean that candidate was poor, not that the whole episode has no usable promo.

For a more automated new-input run, use `--mode api`. Its pool is up to ten non-overlapping candidates per episode and it uses the same schema rules. No live provider call was made during this delivery; tests cover the integration with mocked responses only.
