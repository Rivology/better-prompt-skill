# Building software projects with Claude Code (refreshed 2026-10-28)

Use this when the rough prompt asks to build an app, site, tool, script, or a sizeable feature in an
existing codebase. A project prompt needs more than a task prompt: a written definition of the product,
a sequence of small verified steps, and a way to resume across sessions.

Sources: Anthropic, "Best practices for Claude Code" and "Common workflows" (code.claude.com/docs);
"Keep Claude working toward a goal" (/goal docs); Justin Young, "Effective harnesses for long-running
agents" (Anthropic Engineering, 2025-11-26).

## First, size the project

- **Small**: fits in one sitting. One site, one feature in an existing codebase, one small tool or script.
- **Large**: several components (e.g. accounts + data + deploy), many features, or the user will come back to
  it over several sessions.

Match the process to the size. Heavy machinery on a small project makes the prompt longer and the work slower
without making it better.

## Every project prompt (small and large)

1. **Spec or interview.** If the user hasn't decided what they want (features, users, platform), the prompt is
   an **interview**: "Interview me with multiple-choice questions until you could write the spec, then write
   SPEC.md. Don't write code yet." If they have, state the spec in the prompt itself: the pages, commands or
   behaviors, in a few lines.
2. **Stack and constraints.** New project: a simple, well-known stack (assumed, marked as such) unless the user
   named one. Existing codebase: "follow the patterns already in the repo; no new dependencies without asking."
3. **First milestone and scope.** Name the first working version and what's out of scope for now. Use
   "be ambitious: …" only when the user wants the full version.
4. **Test like a user.** For a UI, run it and check it in the browser (screenshots) or with `/verify`; for a CLI,
   run it on a realistic sample. Start with the thinnest slice that runs end to end.
5. **Checks for this kind of project's risks**, whatever its size. Name the specific way it could fail and
   how Claude proves it doesn't. For example:
   - accounts, login, payments, user data → password hashing, secrets kept out of code, access checks, and an
     independent security review of the diff;
   - bots, schedulers, apps that store state → survives a restart, no duplicate or missed actions, timezones;
   - tools that move, rename or delete files → a dry-run mode, edge cases (name clashes, hidden files, odd
     extensions), and a test on a copy rather than the real folder;
   - anything that takes user input or calls an API → bad input and failure handling.
6. **Done when** the milestone works and the risk checks pass, with evidence: "Done when: the site builds, all
   pages load, and you've shown screenshots at phone and desktop widths."

That's the whole prompt for a small project: no feature file, progress file or per-feature commits.

## Add these only for large or multi-session projects

7. **Feature list with pass/fail checks** in a file (e.g. `features.json` with a `passes` field). Tests in that
   list are not edited or deleted to make things pass.
8. **One feature at a time**: implement, run its check, commit with a descriptive message.
9. **Progress file** (done, next, known issues) and a one-line run command, so a new session can resume.
10. **Independent review** of the whole milestone: a fresh subagent or `/code-review` against SPEC.md,
   "report gaps that affect correctness and skip style".
11. **/goal** for long runs: "the MVP features in features.json all pass, the app runs with one command,
    and a review against SPEC.md found no correctness gaps."

## Tools worth naming in the prompt (only when they help)

- **Plan mode** (Shift+Tab): Claude proposes a plan and edits nothing until approved. Good for changes to
  an existing codebase.
- **/goal <condition>**: Claude keeps working until a separate model confirms the condition holds.
- **/verify**, browser screenshots: check the running app, not just tests.
- **/code-review** or a review subagent: a fresh reviewer that didn't write the code.
- **Worktrees** (`claude --worktree name`): parallel sessions on separate branches.
- **/rewind** and git commits: cheap to try the bolder approach and roll back.
