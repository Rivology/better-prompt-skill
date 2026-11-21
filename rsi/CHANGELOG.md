# Versions judged by the v2 loop

| Date | Candidate | Change | Result | Decision |
|---|---|---|---|---|
| 2026-11-21 | v22 | Protect what works in overhauls; name the choices that are the user's; a named bar becomes a side-by-side check; Claude Code playbook | Own checks: +0.042 per case on 24 held-out real cases (p = 0.004). **Independent pairwise judges** (the first loop's rubric, never shown the checks or the change, each pair in both orders), 41 real cases: v21 preferred, 56 verdicts to 26. v22 added question rounds and approval stops where the user had already handed the choice over, and thinner done-checks. | REJECT |
| 2026-11-21 | v23 | v22 plus: ask only when a choice is really open and not delegated; keep every specific check | Independent pairwise judges, 57 cases (41 real + 16 of the first loop's own tests): +0.06/10 (p = 0.14); real cases +0.07 (p = 0.12), 45 verdicts to 36; the first loop's tests 7 to 25 on verdicts, with equal mean scores. A tie. | REJECT (no clear gain) |
| 2026-11-21 | projects reference | `claude-projects.md`: decision cards, threads, PR watching, schedules, device access, memory | 10 project requests written by an independent agent, 2 draws each, independent pairwise judges. First draft vs v22: −0.14/10, 14 verdicts to 22. Revised draft (with v23) vs v22: −0.28/10, 6 to 30. Judges: more placeholders for facts the project already knows, scope creep and weaker checks. Without the reference, v22 already used project capabilities when the request said it ran in a project. | REJECT |

Lessons:
1. A loop judged only by checks its author wrote will pass its author's change. The independent pairwise guard is now part of the keep rule.
2. Asking more is not safer: the user's bad uses came from silent choices, but adding questions where they had delegated lost more than it gained.
3. More instructions about capabilities crowded out verification, which is what judges reward most.

The rejected drafts are kept in `research/candidates/v23/` as a starting point for later cycles. The benches in
`rsi/bench/` (synthetic, no private prompts) are reusable.
