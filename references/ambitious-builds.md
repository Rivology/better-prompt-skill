# Ambitious and showcase builds (2026-11-02)

Use this when the user wants the result to impress, not just to work: "the most impressive", "really cool",
"stunning", "wow my club", something to share or show off. It changes the shape of the project prompt.
Still use `project-building.md` and `visual-design.md` for facts, stack and testing, and still ask for or
placeholder the facts only the user knows.

Source: an analysis of 12 of the most impressive public Opus 5.5 builds (games, simulations, explorable sites,
long autonomous runs). Most started from a short prompt. What they had in common was a high bar, a check that
decided when the work was done, room to work without stopping to ask, and a version that worked at every step.

## Shape the prompt around these

1. **A high, concrete bar instead of a first milestone.** Say what would make someone say "wow" here: the
   fidelity, the depth, the one moment people would screenshot or share. Don't write "keep it minimal" or "start
   with a thin slice". Ask for the ambitious version, built in passes: the core wow first, then depth, then polish.
2. **A check that decides when it's done.** Make it objective wherever the domain allows: tests for the rules,
   physics or maths matching the known formulas, legal moves, numbers that reconcile. Add a self-check loop on the
   artifact itself: render or screenshot it, compare it with the bar (and any references the user gave), name the
   weakest part, fix it, and repeat until no clear weakness is left.
3. **Room to decide.** Once the user's facts are in hand, tell Claude not to stop for questions: it resolves
   ambiguities itself and lists the choices it made in the README, so the user can change them later.
4. **Working and shareable at every step.** Keep a version that runs and can be shared (a link, a single folder
   for GitHub Pages) after each pass, so the build never ends half-finished.
5. **Scale it when the setup allows.** In Claude Code, offer a time budget ("use up to N hours; keep improving
   until the self-check finds nothing clear"), parallel subagents for separate parts, and a short progress log.
   Mark these as optional, because they depend on the environment.

## Done when (adapt to the build)
The checks pass. The last self-check round found no clear weakness against the bar. It runs at the target sizes
(desktop and phone, or the projector), with screenshots shown. The README lists the decisions Claude made and how
to share or host it.
