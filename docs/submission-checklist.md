# Before submitting

1. Read the two-page solution PDF and run the demo yourself. Review the code and decisions you will explain in interview.
2. Publish ONLY the `promo-scout` code directory to your own GitHub repository, or upload `Promo_Scout.ipynb` to Colab and enable reviewer access. The runtime has no package dependencies. Public prototype repository: https://github.com/Ruthwik2/kuku-promo-scout
3. Upload the solution PDF and the raw-outputs folder to the designated evaluation channel. The raw outputs contain confidential excerpts: do not put them in a public GitHub repository or an indexed site. Use Kuku's submission link/access instructions for reviewers.
4. Include BOTH the unedited `baseline` output and the separately labeled assisted review/output. Do not label assisted judgments as an unattended model run or human evaluation.
5. Supply your name, roll number, branch and Problem 1 in the placement-cell form. No identity details have been guessed.
6. Optional: record an under-three-minute walkthrough in your own voice, following the outline.
7. Test all submission links from an appropriate reviewer session. Do not submit the ChatGPT download links as if they were universally accessible hosted prototypes.

## Package map

- `promo-scout/`: public-safe source, tests, synthetic example, notebook and instructions.
- `private-output/baseline/`: raw full-pack offline JSON/CSV, one file per episode and coverage manifest.
- `private-output/assisted_review.json`: AI-assisted decisions, including rejected candidates and source hashes.
- `private-output/reviewed/`: validated 19-promo AI-assisted shortlist and CSV.
- `private-output/top-10.md`: readable proposed posting order, timestamps and rationale.
- `Kuku_Solution.pdf`: two-page solution document.
- `validation/`: unit-test log, full-pack validation and HTTP checks and the browser-check limitation.

The original screenplay ZIP is deliberately excluded. Use the copy Kuku supplied when rerunning the real pack.
