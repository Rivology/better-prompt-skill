# Launch kit for ambitious builds

Use this together with `ambitious-builds.md` when the user wants something at the level of the best public
work and it will run in Claude Code. The best public builds didn't come from clever wording. They came from:
- the right source material or technique;
- fresh-eyes review against references, round after round;
- hours of resumable work;
- on Opus 5.5, a lead agent with parallel builders.

So the rewrite hands over a whole launch kit: the prompt carries all of it, and the reply adds a short note on how to
launch it. On claude.ai, keep sections 1, 2 and 5, with review done by Claude itself between passes, and drop the rest.

Everything here was measured on Claude Opus 5.5 (2026-11-03). Effort, limits and the work split differ by model, so
read `models.md` and take those three from the target model's section.

## The prompt includes

1. **The bar, and where its quality comes from.**
   - Name the reference works: the user's first, then up to 3 of the best public works of this kind, if such
     works exist. If the task has no public equivalent, the bar is the user's own best past result and a measured
     target.
   - If the user wrote "like X" or "similar to X" and X isn't certain, ask which X (one question).
   - Before building, Claude studies each reference and writes down where its quality comes from:
     - source material (a real scan, a dataset, recordings);
     - technique (a specific renderer, physics model or algorithm);
     - craft details (line weights, density, motion);
     - effort (rounds, agents).

     Then it reproduces the method, not just the look. If a reference's richness comes from a real artifact (for
     example, a map made by reading a real 1819 engraving), it finds the equivalent source for this project first,
     or researches the proper technique, before generating anything.
2. **A finish line that decides "done"**, written as the prompt's "Done when": one end state, how to prove it,
   and what must not change.
   - The proof is objective wherever possible: tests, counts, frame rate, numbers that reconcile.
   - For anything that can be rendered, the proof includes a side-by-side of the build next to the references, at
     the same size and crop. For work with nothing to render, it is the measured result against the baseline.
3. **A progress file** (`PROGRESS.md`) holding the plan, what's done, the next step, decisions, time used and
   "needs the user". It's updated after every round, so a stopped run picks up where it left off.
4. **A work split, sized to the model** (`models.md`).
   - Name the parts that are independent (research and data, a rendering technique, content, audio, tests) and the
     files each one owns.
   - Opus 5.5: a lead agent owns the spec, the integration and the final call, and subagents take the independent
     parts, each with a contract (inputs, outputs, file paths and a done-check).
   - Fable 5.2, or model unknown: don't prescribe a lead or a number of subagents. Say that a subagent is worth its
     cost only for a part that shares no files with the others.
   - The build is Claude's to shape, so include the ownership sentence from `models.md` and ask for a list of
     everything changed at the end.
5. **Review rounds.**
   - After each build round, a reviewer that hasn't seen the code looks only at renders. It compares them with the
     references at the same size, and names the three biggest visible differences in order.
   - The lead fixes the biggest difference first.
   - Stop when a round finds no clear difference at the viewing distance that matters, or when the budget runs out.
6. **A time limit and a stop rule.** The limit is the user's call: use their words if they gave one, otherwise
   ask for it with the other questions ("finish by when, or how many hours at most?"). If you can't ask, write
   "(assumed: up to 4 hours; change if not)". At the limit the run stops with a working build. Spend early rounds
   on the method and late ones on polish.
   - Don't write a token number into the prompt. On Fable 5.2 the size of a written budget changes what the run
     spends, and in our 2026-11-03 benchmark (Opus 5.5) the runs' own token estimates came out 2–4× low.
   - Cap the rounds: at most 6 review rounds, unless the user raises it.
   - At the limit, report the time used and what is left.
   - Add the finishing paragraph from `models.md`, so the run works through ordinary obstacles and stops only for
     the user, a risky step or a deliberate blocker.
7. **What only the user can do**, asked for before the run: keys, accounts, a domain, assets or licences they own.
   Anything else that would need the user mid-run goes into `PROGRESS.md` under "needs the user", and the run
   carries on with what doesn't depend on it.
8. **A final report for someone who hasn't watched the run:** what was built and how to open it, what was checked
   and what wasn't, the decisions made, and what needs the user, with the key points first and in plain words.

## The reply adds
- A short note on launching it, with the effort level and the cost, both taken from the target model's section in
  `models.md`. Label every number with where it came from. For example, on Opus 5.5: "This is built to run for
  hours. Say *start it* and I'll launch it as its own session. On Opus 5.5 our one test build scored about 2.5
  points higher at max effort than at medium and cost 3 to 10 times more; full launch-kit runs at max used 6–9M
  tokens over about 4 hours. For a cheaper run, say *single build*: one session without the work split (about 1.5M
  tokens and 2 hours at max in that test, scoring about a point lower)." On Fable 5.2: "Start it at
  high effort, where Anthropic says most of the gain already is. Nobody has measured this kit on Fable 5.2 yet, so I
  can't give a cost; the Opus 5.5 runs are the only reference." Then a pointer to `PROGRESS.md`.
- Launch the session at the effort level you named. If you can't set it for the new session, ask the user to set it
  before it starts.
- In Claude Code the user can also type the finish line as `/goal <condition>` in the new session, so a separate
  model checks it after every turn. Give that line here, in the note; inside the prompt's text it would do nothing.
- This note replaces the usual "Want me to run this prompt now?" line: a launch-kit prompt should not be run inside
  the current session.
