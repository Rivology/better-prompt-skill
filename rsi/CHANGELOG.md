# Versions judged by the v2 loop

| Date | Version | Change | Held-out result | Decision |
|---|---|---|---|---|
| 2026-11-21 | v22 | Protect what already works in overhauls; name the choices that are the user's (deliverable, unit or mode, how much at once); a named bar becomes a side-by-side check; new `references/claude-code.md` (Claude Code methods, overhauls, feedback loops, Claude projects) | 24 held-out real-use cases, 1 rewrite per side, 2 blind judges: check pass rate +0.042 per case (p = 0.004); U4 bar 0.33 → 0.75, U3 protect-what-works 0.73 → 0.90, U2 owner-choices 0.90 → 0.94; no check fell; rewrites 7% shorter; judge agreement 0.85–1.00 per check | KEEP (pending merge) |

Caveats for v22: the checks and the change were written in the same session by the same author, so U3 and U4 measure
exactly what the change targets. The held-out case-specific checks didn't move (0.29 → 0.29). Rewriters and judges
were one model at one effort level, with one rewrite per case.
