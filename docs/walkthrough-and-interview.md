# Three-minute walkthrough outline

Speak in your own words after running and understanding the prototype.

**0:00–0:25 — Problem and scope.** Explain why you chose promo discovery: the output has inspectable timestamps and can save an editor scanning time. This prototype proposes continuous clips; it does not edit videos or predict virality.

**0:25–1:00 — A fresh run.** Start `server.py`, upload the ZIP, show 50 episodes and the offline label. Explain elapsed time versus overlapping camera/dialogue tracks. The 20–60 second limit and spoken-line boundaries are enforced in code.

**1:00–1:45 — The stronger shortlist.** Open the assisted review JSON, inspect a leading clip and its source timestamps. Explain how the opening hooks the viewer and the ending cuts before the decision. Expand dialogue. Compare the original baseline if asked; the improved cut was found during AI-assisted source review, not automatic keyword discovery.

**1:45–2:15 — An honest failure.** One rejected baseline candidate starts well but ends on another insult. The heuristic likes the question mark; it is not a genuine narrative cliffhanger. Show its rejection rationale. Mention that many high-quality alternatives could still be missed.

**2:15–2:40 — New model/new input.** Show the CLI's base URL/model settings and the validator. The model picks IDs, while code maps them to source times. The saved review is hash-bound and cannot be reused on another show.

**2:40–3:00 — Evidence and next step.** Mention 15 unit tests, full-pack boundary checks and no human/CTR validation. The next experiment is an editor-blinded ranking study, followed by a controlled creative A/B test.

# Questions to prepare for

- Why code for timestamps? To prevent invented cut points and enforce measurable constraints.
- Why not send all 50 scripts at once? Per-episode bounded candidate pools reduce context and make failures attributable. They also limit recall.
- Is offline mode AI? No. AI was used in development and assisted editorial review; the runtime AI adapter is optional and not live-provider-validated here.
- Why can a 100 score still fail? It is a subjective rubric score, not a probability. Acting, framing, audience fit and spoilers are unseen.
- How do you avoid false self-containment? Exclude loglines from scoring; ask the model to judge only the clip; have a new viewer summarize it without context.
- How would you scale? Parallel episode jobs, cache by source+prompt+model, sliding-window features, bounded provider concurrency, retries and a review queue. These are future work.
- What did AI get wrong? The development assistant initially attached a cliffhanger rationale to an earlier tail event rather than the actual cut boundary. Source inspection exposed this; assisted review now names explicit source evidence and preserves the raw baseline separately. Keyword question detection also overvalued a rhetorical taunt.
- What do tests prove? Structural correctness, parsing and error handling. They do not prove that a promo will attract viewers.
