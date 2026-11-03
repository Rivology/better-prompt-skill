# Launch kit for ambitious builds (candidate, 2026-11-03)

Use this together with `ambitious-builds.md` when the user wants something at the level of the best public
work and it will run in Claude Code. The best public builds didn't come from clever wording. They came from:
- a lead agent with parallel builders;
- fresh-eyes review against references, round after round;
- the right source material or technique;
- hours of resumable work.

So the rewrite hands over a whole launch kit: the prompt carries all of it, and the reply adds one line on how to
launch. On claude.ai, keep sections 1, 2 and 5, with review done by Claude itself between passes, and drop the rest.

## The prompt includes

1. **The bar, and where its quality comes from.**
   - Name the reference works: the user's first, then the 2–3 best public works of this kind.
   - If the user wrote "like X" or "similar to X" and X isn't certain, ask which X (one question).
   - Before building, Claude studies each reference and writes down where its quality comes from:
     - source material (a real scan, a dataset, recordings);
     - technique (a specific renderer, physics model or algorithm);
     - craft details (line weights, density, motion);
     - effort (rounds, agents).

     Then it reproduces the method, not just the look. If a reference's richness comes from a real artifact (for
     example, a map made by reading a real 1819 engraving), it finds the equivalent source for this project first,
     or researches the proper technique, before generating anything.
2. **A finish line that decides "done"**, written as a `/goal` condition: one end state, how to prove it, and what
   must not change.
   - The proof is objective wherever possible: tests, counts, frame rate, numbers that reconcile.
   - The proof always includes a side-by-side of the build next to the references, at the same size and crop.
3. **A progress file** (`PROGRESS.md`) holding the plan, what's done, the next step, decisions, budget used and
   "needs the user". It's updated after every round, so a stopped run picks up where it left off.
4. **A work split.**
   - The lead agent owns the spec, the integration and the final call.
   - Subagents take independent parts (research and data, a rendering technique, content, audio, tests), each with
     a contract: inputs, outputs, file paths and a done-check.
   - Run them in parallel only when they don't write the same files.
5. **Review rounds.**
   - After each build round, a reviewer that hasn't seen the code looks only at renders. It compares them with the
     references at the same size, and names the three biggest visible differences in order.
   - The lead fixes the biggest difference first.
   - Stop when a round finds no clear difference at the viewing distance that matters, or when the budget runs out.
6. **A budget**: wall time and tokens, for example "up to 4 hours and about 2M tokens". Spend early rounds on the
   method and late ones on polish.
   - Make time the hard limit. In the 2026-11-03 benchmark, runs' own token estimates came out 2–4× low.
   - Cap the effort too: at most 6 review rounds and about 8 subagents in total, unless the user raises it.
   - Stop at the time limit with a working build, and report the time used and the token estimate, labelled as an
     estimate.
7. **What only the user can do**, asked for before the run: keys, accounts, a domain, assets or licences they own.
   Anything else that would need the user mid-run goes into `PROGRESS.md` under "needs the user", and the run
   carries on with what doesn't depend on it.

## The reply adds
- One line on launching it: "This is built to run for hours: say *start it* and I'll launch it as its own
  session." Then a pointer to `PROGRESS.md`.
