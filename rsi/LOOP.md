# Running one improvement cycle

`L` below means `python3 <repo>/rsi/loop.py`. Private data goes in `$BP_DATA` (default `~/better-prompt-runs/rsi2`).

## 1. Learn what went wrong
1. `L harvest`: lists the uses with no label yet. For each one that has a session, give the labeler
   (`briefs/labeler.md`) the rough prompt, the rewrite and the user's next messages from the transcript. Collect its
   JSON lines in a file, then run `L label <file> --guards`. This turns bad uses into cases and good ones into guards.
2. `L northstar`: has the share of bad uses fallen since the last version?
3. Read the new bad cases together. Name the pattern they share in one sentence. That pattern is the hypothesis.
   Write it down with its evidence (case ids, the user's words) and a prediction: which checks should move, which way,
   and by roughly how much.

## 2. Make one change
Copy the live skill (SKILL.md plus references) into a candidate folder and make one focused change there: a rule, a
routing line or a reference section. Make it general, never special-cased to a test request. Keep SKILL.md under
about 150 lines.

## 3. Test it
1. `L prepare --baseline <live dir> --candidate <candidate dir> --split heldout --name <name>`. Use `--split all`
   only to report, never to decide. Give folders neutral names (not "old" or "new").
2. Start one rewriter per `jobs_A/BRIEF.md` and `jobs_B/BRIEF.md`. Split a long jobs file across two rewriters per
   side by item number. All rewriters run on the same model and effort level.
3. `L lint <run>/rewrites/*.md`: a free check for missing prompts, missing Done when or shouting.
4. `L blind <run> --judges 2 --batch 41` writes one sealed folder per judge batch under `<run>/judging/`. Give
   each folder to one judge, which reads only `judge.md`, `checks.md` and `batch.md` there and writes
   `verdict.json` next to them. Judges are told to open only their folder, never the run folder that holds the unblinding key.
5. `L score <run> --hypothesis "..."` prints KEEP or REJECT with its reasons.

## 4. Decide and publish
- **KEEP:** copy the candidate over the live skill, bump `VERSION`, and open a pull request on a `loop/v<N>`
  branch. Merging it publishes the version (the claude.ai loader reads main), and merging is the user's call. Then check the prediction you wrote in step 1.
- **REJECT:** record it. Retry the same idea only with a materially different approach.
- **Read some rewrites either way.** A score you haven't read the transcripts behind can be a grader bug.

## Monthly
- **Judge health:** agreement per check from recent `result.json` files. A check under 70% agreement is rewritten or
  dropped, with the user's OK.
- **Human spot check:** show the user 5 judged rewrites with the verdicts, and record whether they agree.
- **Outcome check** (optional, expensive): run v1's executor-based check on the fixture apps for the live version
  against the one from three keeps ago.
- **Docs refresh:** read the Anthropic pages listed in `research/` and record what changed. A material change
  becomes a hypothesis for the next cycle. It doesn't go live without one.

## Never, in a cycle
Change `checks.md`, the judge brief or the keep-rule constants in `loop.py`. Those are the user's call, because a
loop that can change its own grader can make anything pass.
