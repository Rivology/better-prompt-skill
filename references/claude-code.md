# Claude Code methods for long and agentic prompts (2026-11-21)

Read this when the prompt will run in Claude Code or in a Claude project and the work is long or agentic. A short
task needs none of it. Model-specific advice (effort, finishing paragraph, delegation, ownership) stays in
`models.md`. Sources and dates: `research/claude-code-methods-2026-11.md` in the skill's repo. Every method here is
documented advice; none was measured by this skill.

## Pick the levers, don't list them all

A senior prompt uses the two to four methods this task needs, each with its reason, in plain sentences. Choose them
like this:

| If the task… | Put this in the prompt | Why |
|---|---|---|
| is open (the user hasn't settled what gets built) | "Interview me with the AskUserQuestion tool until you could write the spec, then write SPEC.md; build from it in a fresh session." | Choices stay the user's; a clean session builds better than a long one [BP] |
| changes many files or the approach is unclear | "Explore and plan first (plan mode); show me the plan before editing." Skip this when the diff fits in one sentence. | Cheap to correct a plan, expensive to correct code [BP] |
| has a finish line that can be checked | the check itself in "Done when", and in the reply a `/goal <condition>` line for unattended runs | A separate evaluator re-checks after every turn [BP] |
| must never skip its check (tests, lint, a build) | "Add a Stop hook that runs `<check>`" (or name an existing one) | Hooks are deterministic; instructions are advisory [BP] |
| spans sessions or may hit compaction | a progress file (plan, done, next, decisions, needs the user), commits as checkpoints, and "start each session with git log, the progress file and a quick end-to-end check" | Long runs fail by declaring victory early or losing state [HARN] |
| is a multi-feature build | a feature list in JSON, each item `"passes": false`; only the flag changes; tests are never edited to pass | Models edit JSON less destructively, and it stops early "done" [HARN] |
| has a quality bar | a reviewer in its own context that sees only the result and the reference and names the biggest gaps, round after round | Self-review in the same context is weaker [BP, TALK] |
| needs wide reading (docs, logs, a big codebase) | "use subagents for the reading and keep their summaries short" | Keeps the main context clean [BP, CTX] |
| has parts that share no files | worktrees or parallel subagents, one per part, each with its inputs, outputs and done-check | Parallel only pays when parts are independent [BP] |
| repeats one change over many files | headless `claude -p` with an allowlist, tried on 2–3 files first | [BP] |
| will run unattended | the exact actions that need a go-ahead, and that everything else (reads, local edits, retries) needs none | Vague caution gets over-applied [BP, models.md] |

Also worth one line when it fits: keep CLAUDE.md to what Claude would get wrong without it, and move repeated
workflows into a skill [BP]; after two failed corrections, `/clear` and rewrite the prompt instead of a third
correction [BP].

## Overhauls of something in use

These are the riskiest prompts the user sends, so they get the most structure:
1. **Diagnose before building:** what is wrong today, in the user's words and in evidence (logs, the user's
   complaints, a run of the current thing). The fix aims at that, not at a general wish for "better".
2. **Settle the user's choices first** (see SKILL.md step 2): the deliverable, the unit or mode, how much at once.
3. **Protect what works:** record today's behaviour, change it in steps that each leave it usable, one feature at a
   time, and finish with the old main path checked end to end.
4. **Cap the first version.** "Ambitious" sets the bar for quality, not the amount shipped at once. A small first
   version the user tries, then the next.

## Prompts that build or overhaul a feedback / self-improvement loop

A loop improves only what it measures, so the prompt asks for the measurement first [EVAL, HILL]:
- Test cases come from real use, especially the uses that went badly, with balanced cases that went well so the loop
  doesn't over-correct ("one-sided evals create one-sided optimization").
- Grading: deterministic checks where possible; otherwise yes/no checks written from real failures, judged blind,
  with two judges or a human spot check to show they agree. Watch for judges preferring length.
- A held-out set nothing was tuned on decides each change; make one change at a time, keep it only if held-out
  improves, and revert when train rises but held-out stays flat.
- One number that matters, tracked per version on real use (for example the share of uses the user had to correct).
- Read the transcripts behind a score before trusting it.

## Prompts for work inside a Claude project (coordinator, threads, shared memory)

When the prompt sets up or runs inside a project where a coordinator starts threads and they share memory:
- **One goal per thread:** split the work into threads by goal, each with its own finish line. Say which threads
  depend on which, so a thread can tell another when its part is done.
- **Shared memory holds what a new thread would otherwise have to ask:** standing preferences, decisions and where
  things live. It doesn't hold progress, which belongs in the thread's checklist and files.
- **Files that outlive a thread** (plans, reports, private data) go in the project's shared files, never in a public repo.
- **Checkpoints for the person:** a checklist they can glance at, one decision card per real choice (with a
  recommended option), and a short reply only for a result, a blocker or a question. Irreversible steps (merging,
  publishing, deleting, messaging others) wait for their word.
- **Long runs** follow the project's saved rule on where they run (their computer, CI, or the cloud), so a thread
  nobody is watching does the right thing.
