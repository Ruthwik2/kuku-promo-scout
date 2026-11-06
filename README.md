# Promo Scout

A small editorial tool for Kuku Problem 1: find continuous 20–60 second promos in timestamped microdrama screenplays. Python 3.10+ and a browser are enough; the default run needs no packages, credentials, or internet.

## Start in under a minute

```bash
cd promo-scout
python3 server.py
```

Open http://127.0.0.1:8765. Upload the original screenplay ZIP with **Analyze ZIP**, or use **Open results JSON** to inspect an existing run. The ZIP upload runs the **offline heuristic**. It does not call an AI model. On Windows, use `py` if `python3` is unavailable.

For the supplied reviewed results, from inside `promo-scout`:

```bash
python3 server.py --results ../private-output/reviewed/ranked_promos.json
```

The HTML also opens directly as a file for JSON inspection; ZIP analysis requires the Python server. Approvals persist for the browser session only: export decisions before closing it.

## Repeat the full-pack run

```bash
python3 scout.py "/path/to/original-scripts.zip" --out runs/my-run --expected-episodes 50
```

Accepts a ZIP, directory of TXT files, or one TXT screenplay. Use a fresh output folder each time. JSON, CSV, per-episode outputs, coverage, hashes, and parse errors are written there. Exit status 2 means incomplete coverage or API errors. Do not present a partial run as complete.

Try the original synthetic example (safe to share publicly):

```bash
python3 scout.py examples --out runs/demo
python3 -m unittest discover -s tests -v
```

## Three clearly separated modes

1. **Offline baseline:** all valid source-boundary windows, keyword scoring, overlap suppression, at most three picks per episode. Fast and reproducible, but weak at narrative meaning.
2. **AI-assisted review:** a saved ChatGPT/editor judgment is validated against exact source hashes and candidate IDs. The supplied review inspected the leading candidate from each episode, and additional source passages for four recuts. This is not an automated API run or an independent human evaluation.
3. **API model:** a replaceable Chat Completions-compatible model reviews a diverse pool of up to ten candidates per episode. This adapter is tested with controlled responses, but was **not tested against a live external model**. Models must support the request format, temperature=0, and JSON text responses. Provider compatibility may require adjustment.

```bash
export LLM_BASE_URL="https://YOUR-PROVIDER/v1"
export LLM_MODEL="YOUR-MODEL"
# Set LLM_API_KEY privately in your shell if the provider requires it.
python3 scout.py /path/to/scripts.zip --mode api --out runs/model-run
```

This sends selected screenplay content to the configured endpoint. Use only an authorized provider. A local compatible server can use http://localhost:PORT/v1 with no key. API failures are logged, not silently replaced with offline scores. Raw successful HTTP responses are retained even when their JSON/schema is rejected. Request/network failures are recorded in the manifest.

To reproduce the supplied assisted shortlist:

```bash
python3 review.py /path/to/original-scripts.zip ../private-output/assisted_review.json --out runs/reviewed
```

A fresh input needs a fresh review. See `docs/review-workflow.md` for the free-tool review process and schema. The saved review is not a pretrained model and is never reused on different scripts.

## How it works

- Parse overlapping camera/action/dialogue tracks without adding their durations together.
- Enumerate 20–60 second windows starting on dialogue/action/sound events and ending at source event boundaries.
- Reject starts or ends inside any spoken line. Partial camera/action shots remain possible: editor inspection is necessary.
- Score opening hook and ending signals; use only clip dialogue for standalone-context features. Loglines never contribute to the score.
- Suppress candidates overlapping at least 65% of the shorter clip; retain a diverse shortlist.
- Validate model IDs and score types. Code owns timestamps; the model can only select known clips.
- Let an editor inspect source evidence, approve, and export. No video editing is performed.

Offline score = 7×hook + 7×ending + 4×context + 2×pace − scene penalty (features 0–5). Assisted/API score = 7×hook + 7×cliffhanger + 6×standalone. These are subjective rubric scores out of 100, **not probabilities**. Do not compare different modes as calibrated measurements.

## Known limits

Continuous clips only. English keyword features are genre-biased. Rhetorical questions, abstract threats, and reaction shots can be false positives. A strong window missed by the coarse shortlist will not reach the API model. Full-source quality recall, CTR, retention, and frame accuracy have not been measured. Dialogue records containing continuation ellipses can still be semantically incomplete even if not cut in the middle of a timed line.

The current enumerator and per-window scoring are suitable for short episodes, not feature-length scripts. A production version should use sliding windows, incremental features, episode queues, response caching, bounded parallelism and provider-specific retries. Those improvements are proposals, not implemented features.

## Confidentiality and submission

Publish only the `promo-scout` directory, which contains code and a synthetic example. Do not publish the original pack or `private-output`: it includes screenplay excerpts. Share real outputs only through Kuku's designated evaluation channel. The notebook can be uploaded to Colab; the code directory can be uploaded to a GitHub repository with these run steps. Public prototype: https://github.com/Ruthwik2/kuku-promo-scout

Open the notebook: https://colab.research.google.com/github/Ruthwik2/kuku-promo-scout/blob/main/Promo_Scout.ipynb

The two-page solution PDF is in the parent package. The checklist and walkthrough in `docs` explain what to review and submit. Add your own name/roll number/branch in the submission form and record the optional video in your own voice. Understand and verify the work before submitting.
