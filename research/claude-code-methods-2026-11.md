# Claude Code methods for senior-level prompts (researched 2026-11-21)

Sources (all opened 2026-11-21):
- **[BP]** Claude Code docs, "Best practices" (code.claude.com/docs/en/best-practices; live docs, no date).
- **[HARN]** Anthropic Engineering, "Effective harnesses for long-running agents" (published 2025-11-26, modified 2026-10-18).
- **[CTX]** Anthropic Engineering, "Effective context engineering for AI agents" (published 2025-09-29, modified 2026-10-18).
- **[TIPS]** Claude Help Center, "Claude Code power user tips" (support.claude.com/en/articles/14554000; "updated over a week ago").
- **[TALK]** AI Engineer World's Fair 2026, "Claude for long-horizon tasks" (talk page; cites Anthropic posts dated 2026-04-08, 2026-05-19, 2026-06-23).
- **[EVAL]** Anthropic Engineering, "Demystifying evals for AI agents" (published 2026-01-09, modified 2026-10-18).
- **[HILL]** Arize, "Claude's hillclimb loop for AI agents" (2026-10-02), quoting an Anthropic post of 2026-09-28.

"Measured" means the source gives a number. Everything else is documented advice or practice.

## Methods a senior engineer's prompt uses, and when

| Method | What it does | When it pays off | Source | Measured? |
|---|---|---|---|---|
| Give Claude a check | A test, build, screenshot or script that comes back pass or fail; ask for the evidence | Always; TIPS calls it the single most impactful practice | BP, TIPS | no |
| Verifier in its own context | A separate agent or `/goal` evaluator grades against a rubric, and the builder loops until it passes | Long or unattended runs; quality bars | BP, TALK | no |
| `/goal <condition>` | A separate evaluator checks one measurable end state after every turn | Unattended runs with a clear finish line | BP | no |
| Stop hook running the check | Deterministic: the turn can't end until the check passes | Must happen every time with zero exceptions | BP, TIPS | no |
| Interview then spec | "Interview me in detail using the AskUserQuestion tool", then write SPEC.md and build in a fresh session | The user hasn't settled what gets built | BP, TIPS | no |
| Plan mode | Explore, plan, implement, commit; skip it when "you could describe the diff in one sentence" | Multi-file or unclear changes | BP | no |
| Pushback | "Grill me on these changes", "prove to me this works" | Before merging a large change | TIPS | no |
| Feature list as JSON | Every item starts `"passes": false`; agents only flip the flag and never edit tests | Multi-session builds | HARN | no |
| Progress file + git as memory | Start each session with git log, the progress file and a basic end-to-end check | Anything spanning sessions or compaction | HARN, CTX | no |
| Short CLAUDE.md | Test each line: "Would removing this cause Claude to make mistakes?"; workflows go in skills | Projects with repeated sessions | BP, TIPS | no |
| Subagents for reading | Keep research and verbose output out of the main context (summaries of about 1,000 to 2,000 tokens) | Wide searches, log reading | BP, CTX | no |
| Writer and reviewer | One session builds, a fresh one reviews and flags only correctness and requirement gaps | Changes worth a second look | BP | no |
| Worktrees and parallel sessions | `claude --worktree`; `/batch` fans a migration out over subagents, each in its own worktree | Independent parts that share no files | BP, TIPS | no |
| Headless fan-out | `claude -p` with an allowlist; refine on 2 to 3 files before running all | Repetitive changes over many files | BP | no |
| Auto mode / permission allowlists | The default mode on recent versions; a classifier blocks scope escalation | Long runs without constant approvals | BP | no |
| Clear, don't pile on corrections | After two failed corrections, `/clear` and write one better prompt | Steering | BP | no |
| Protect what works | Baseline first, keep the app usable at every step, regression check, one feature at a time | Overhauls of a live system | HARN ("leave the repo clean"); our real-use failures | no |
| Hill-climb with a held-out set | Make one change, score it, keep it if held-out goes up, revert if train rises and held-out stays flat | Any self-improving loop, including a product's own feedback system | EVAL, HILL | Arize example only |
| Memory consolidation ("dreaming") | Write notes during the task and consolidate offline; "Raw memory can make an error repeatable" | Assistants that learn across sessions | TALK | no |

## Where the skill falls short today (v21)

1. **Overhauls of a live system get no "protect what works" rule.** Two of your failed uses were overhauls that broke a working app. HARN's discipline (one feature at a time, leave it working, an end-to-end check before new work) is not in the skill outside the large-project framework.
2. **The verifier-in-its-own-context pattern is only in the launch kit.** Any long run with a quality bar should get it, through a fresh reviewer, `/goal` or a Stop hook.
3. **`/goal`, Stop hooks, plan mode and the interview route are mentioned but not chosen.** A senior prompt picks the one lever that fits the task and says why.
4. **No guidance for prompts that run inside a multi-thread Claude project** (coordinator, threads, shared memory, a progress checklist, decision cards).
5. **No guidance for prompts that ask Claude to build or overhaul a feedback loop.** You've asked for this at least four times (Jarvis, better-prompt, book summaries). EVAL and HILL give the senior answer: real-use cases, held-out sets, binary checks calibrated against people, one change at a time.
6. **Choices that are yours get decided silently.** This is the main failure in your real uses. The skill says to ask about choices that are "decisive and unguessable", but it doesn't name the cases where rewrites go wrong: a follow-up that changes the deliverable type, an ambiguous mode ("sometimes through lecture"), modifying something versus making a new one.
