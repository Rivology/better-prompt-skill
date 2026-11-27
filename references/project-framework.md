# Project framework: plan, execute, deploy (2026-11-12)

Use this when the rough prompt asks for a serious software project: one that will be put online, one with several
parts, one the user will come back to over several sessions, or one meant to be at a professional level. It tells
you how to write a prompt that carries the project through three stages. It adds to `project-building.md` (read
that first) and, for a build meant to impress, to `ambitious-builds.md` and `launch-kit.md`. Where they overlap,
keep one line, not two.

Written for Claude Fable 5.2 and **not yet tested on a real build** (see `models.md` section 7). Everything that
differs by model (effort, the finishing paragraph, the ownership sentence, which model a subagent runs on, whether
to plan on one model and build on another) is in `models.md` and only there.

**Where the words go.** A project prompt spends its words on what is being built: the spec, the bar, the risks of
this project. Each item below becomes at most a sentence or two in the prompt, and only the items this project
needs. The explanations and sources here are for you; don't copy them into the prompt.

Where each line comes from:
- **[F52]** Anthropic, "Prompting Claude Fable 5.2" (read 2026-11-12; the page was rewritten after 2026-11-09).
- **[CC]** Claude Code docs, read 2026-11-12: best practices, common workflows, permission modes and auto mode,
  /goal, subagents, worktrees, hooks, sessions. Advice and documented features, mostly without numbers.
- **[BP]** Anthropic, "Prompting best practices" (all models). **[ENG]** Anthropic Engineering, "Effective harnesses
  for long-running agents" (2025-11-26).
- **[P1]** Ethan Mollick's Portals (471 generated 3D worlds; live site and repo opened 2026-11-12). **[P2]** Kieran
  Klaassen and Every (ambient.town, opened; how it was built is second-hand). **[P3]** "nzach", a one-hour
  single-file build with measured numbers, opened. Results someone showed, not tests.
- **[V]** Alex Finn's video "Fable 5.2 just dropped" (2026-11-09): a planning workflow shown on screen; the build it
  leads to is not shown finished.
- **[T]** our deploy check, 2026-11-12: a placeholder page published to GitHub Pages, checked live at phone and
  desktop size, updated, and rolled back. **[R]** gaps a blind reviewer named in this file's first drafts.
- **[AV]** Anthropic (Addy Osmani), "How the Claude Code team thinks about verification" (claude.dev, 2026-11-16):
  the team's own practice, with one measured number (a separate rubric grader, up to +10 points).
- **[W]** Simon Willison: sparqlite (2026-10-16), a 12-hour run judged by 636 of 639 W3C tests; Battle Drones
  (2026-10-20), 1,200 simulated matches cut undecided games from 14% to 0.9%. **[MIG]** Anthropic, "Migrating our
  Messages API to Rust" (2026-11-25): about 98% of tests passed while about a quarter of production inputs matched.
- **[O55]** our benchmark builds on Opus 5.5, 2026-11-03. **[practice]** common practice; nobody tested it here.
  **[skill]** a rule the skill already has in `SKILL.md` or `project-building.md`.

## Size it first

| The project | What the prompt gets from this file |
|---|---|
| **Small**: one sitting, one page or tool, and it goes online | The small-project lines below, a short paragraph added to the `project-building.md` prompt. No stages, no extra files. |
| **Large**: several parts (accounts, data, a server), many features, or several sessions | All three stages, as a prompt with headings. |
| **Showcase** (the launch kit applies) | The launch kit's prompt, plus the questions in item 1 and one paragraph from stage 3. The bar and its review rounds replace the milestones. Nothing here replaces a line about the product: what it shows, what people can do with it, how it must run on the device they open it on. The look of the interface (`visual-design.md`) and what a device that can't run it shows stay in the prompt. A stretch feature is named as one: it comes after the core and its polish, and meets the same speed target or is left out [R]. |

Heavy process on a small project makes the prompt longer and the work slower without making it better [CC, O55].
A project that never leaves the user's machine gets nothing from stage 3 [skill].

**Small-project lines.** Add only these, in the user's voice:
- where it goes: "publish it with GitHub Pages on my GitHub account, in a public repo named …" (item 15) [T];
- access first: "before you build, check that `gh` is installed and signed in; if it isn't, tell me the exact step,
  and if I can't do it, leave me the finished folder and three lines on how to upload it" [R];
- one look before it is public: "show me screenshots before the first publish, and list any wording you wrote
  that I didn't give you; later changes need no go-ahead" [R];
- "nothing private in the repo, and use my GitHub no-reply address for the commits" (item 17) [T];
- the finish line ends on the live link: "Done when: the live link opens at phone and desktop size, with
  screenshots of the live page, it shows a title and description when the link is shared, and the README says
  in three lines how to change the page and put the old one back." [T, R]

## Stage 1: planning (before any code)

1. **Ask the user what only they know.** At most 3 questions through AskUserQuestion, the ones that change what
   gets built; the rest become placeholders or assumptions. The usual ones for a project: who uses it and on what
   device; the two or three things it must do, against what can wait; where it will live and who may see it; what
   it needs that only the user has (an account, a key, a domain, real content); how long the run may take [skill].
2. **Challenge the idea, then settle the open decisions as multiple-choice questions.** For a large project the
   prompt's first step is: "Before planning, tell me where you'd change this idea and which decisions are mine,
   as multiple-choice questions with your recommendation first. Build nothing yet." In the video the model's
   pushback (the request was really three products; pick one) reshaped the project, and it came only after the
   model had built a prototype it then called a mistake [V]. If the user hasn't decided what they want at all,
   this step is the interview: "Interview me until you could write the spec, then write it to SPEC.md" [CC].
3. **A written spec.** `SPEC.md`: who it is for, the screens or commands, the data, what each feature does, what
   is out of scope. It says what the project must do and how good it must be, and leaves layout and internals to
   Claude unless the user has a firm view: the builds that shipped started from a short goal with a quality bar
   [P1, P3], and a rigid, detailed spec was reported to make a result worse [P2, second-hand].
4. **Architecture and stack that fit where it will live.** The deploy target is chosen now, because it limits the
   stack. A static host such as GitHub Pages runs no server and keeps no secret: every file is public [T]. A
   project with accounts, shared data or a paid API needs a named backend service and a list of what the user
   must sign up for, or another target. Ask for the choice, its reason in a line, and the simplest well-known
   stack that fits; the user's named stack wins [skill].
5. **Three to six milestones and a task list, each task with a check that comes back pass or fail** [CC]. The first
   milestone is the thinnest version that runs end to end and is already at its real address (one real piece of the
   main feature, not an empty shell [R]), so the deploy is proved on day one [T]; all three shipped builds went
   live early, Portals at 20 hours of a 12-day build [P1, P2, P3]. Each later milestone is a part of the product a
   user can use, and ends with the user trying it for real before the next one starts; the spec ends with one
   success test for the whole project, in the user's terms [V]. Tasks are the small steps inside a milestone: a
   task gets its check and a commit, and only a milestone gets a review and a release [R]. The task list is a file
   in the repo (`TASKS.md` or `features.json`: task, milestone, status, the check that proves it), written so that
   a new session, or another model, can build from it without the conversation [V, ENG, CC]. Use an outside tracker
   (Notion, Linear) only if the user already works in one [V shows Notion; a file is our choice]. Where a judge
   exists outside Claude's own work, the checks use it: the old system for a rewrite (the same inputs through
   both, outputs compared), a public test suite or standard, many simulated runs, a real measurement. Tests
   Claude writes for its own code share its blind spots [W, MIG].
6. **The risks of this kind of project**, each with how Claude proves it doesn't happen: `project-building.md`
   item 5, plus the release risks in stage 3 [skill].
7. **Standing rules go in `CLAUDE.md`**, for a project of several sessions: the command that runs it, the command
   that checks it, the risk checks, the review rule for each milestone, the go-ahead list, the publish steps and
   the finish line. Later sessions read only the files, so a rule that is in the first prompt and not in them is
   lost [R]; a rule that lives only in the conversation can also be lost when the context is compacted [CC].
8. **A stop for the plan, when someone is there:** "Write SPEC.md and the task list, then stop and show me the
   plan" (plan mode in Claude Code [CC]). Then build from the files in a fresh session [CC]. For a run nobody
   watches, don't stop: decide, write the decisions down, carry on [F52, skill].

## Stage 2: executing

9. **Order of work:** the live skeleton, then one task at a time (build it, run its check, commit), then the risk
   checks, then polish. Each commit leaves a version that runs [ENG, BP].
10. **`PROGRESS.md`**, with what it is for: so a stopped run or a new session can carry on from it. The plan,
    what's done, the next step, decisions, time used, "needs the user", and the one command that runs the project
    [ENG, BP, O55]. Pass/fail checks in the task list are not edited or deleted to make them pass [ENG].
11. **Test like a user, with evidence.** Run it and use it: click through each feature in a browser at phone and
    desktop size; a command-line tool runs on a realistic sample. Ask for the command and its output, or the
    screenshot, not "all tests pass" [CC]. Before each release the running product is checked, and a part that
    fails is left out [P1]. The devices named in the spec are the test targets: a number measured on the build
    machine doesn't prove a phone, so the report says what could not be measured [R]. The way to run and check the
    project is written down as a `verify` skill (`.claude/skills/verify/SKILL.md`; Claude Code uses it before each
    commit, and `/verify` creates one), kept fast and reliable [AV]. A check that still fails after three rounds of
    fixes stops that task and goes in the report instead of a fourth try; a flaky test is fixed, or deleted with
    the reason written down, never skipped, retried or padded with waits [AV].
12. **Fresh-eyes review at each milestone.** One reviewer that hasn't seen the code or the conversation checks
    the build against SPEC.md: "report gaps that affect correctness and skip style". Keep "skip style": a reviewer
    asked to find problems always finds something [CC]. Fix the biggest gap first.
13. **Delegation, in two sentences at most.** No order to delegate and no number of subagents [F52]. Something
    like: "Use a subagent only for a part that shares no files with the rest, for a wide search or long test run
    whose output you don't need, and for the fresh reviewer. Brief it with the goal, the files it owns, the check
    to run and what to send back, in a few lines, because the brief is all it knows." A subagent buys parallel
    work or fresh eyes, "not a smarter answer", and it starts with nothing [CC]. Which model it runs on:
    `models.md`. Parallel builders each get their own worktree [CC].
14. **Only for a build that runs for days or with many agents:** one sentence against process growth: "Every new
    rule or check names the failure it prevents, and at each milestone ask what can be cut." In Portals the
    agents' own rule book grew to 87,500 words, output fell from hundreds of worlds a day to about a dozen, and
    the model did not notice; builders also tuned their work to the judges' fixed screenshots, so judged checks
    (screenshots, reviews) use fresh samples while pass/fail checks stay fixed [P1].

## Stage 3: deploying

**Before the first publish** (it happens in the first milestone):

15. **The target, named, and access checked at the start of the run.** The user's own words if they gave one.
    Otherwise, for a static site, GitHub Pages on the user's own GitHub account, in a repo whose name and
    visibility the prompt states (assumed, marked as such); a project with a backend names the host chosen in item
    4 and leaves GitHub Pages out [R]. The first step of the run is `gh auth status`; if it fails, Claude says the
    exact step and builds on meanwhile [R]. Publish from the `main` branch (the root or `/docs`), not a `gh-pages`
    branch: in auto mode a push to a branch named like a deploy target is judged as a deploy [CC].
16. **The go-ahead for publishing, written into the prompt.** A person signs off on what can't be taken back
    [CC]. Name the exact action [F52]: "Get my go-ahead before the first publish, with screenshots; later updates
    to the same repo need none", or, for a run nobody watches, "Publishing to a new public repo named X on my
    account needs no go-ahead." Whatever costs money, creates an account or sends a message to real people is on
    the go-ahead list too [R]. Add: "If a publish step is refused, finish everything else, leave me one command
    that does it, and say so." In our check the app refused to create the public repo and to make the first push
    although the task allowed both; later pushes to the existing repo went through [T]. Approval typed later has
    to name the action and what it applies to: "Naming the verb alone clears nothing" [CC].
17. **Nothing private goes out.** Before the first push Claude searches the files for keys, tokens, passwords and
    personal details and shows the result. Secrets live in the user's environment or the backend's settings,
    never in the repo; `.env` is in `.gitignore`. In a public repo the commits use the account's GitHub no-reply
    address, because the commit email is public [T]. Anything borrowed (data, images, code) may be republished
    and is credited in the README: Portals' licence check before release found borrowed code its own notes had
    missed [P1].

**At every release:**

18. **Publish with commands that are written down** (README or a `deploy` script) [practice]. On GitHub Pages the
    site is served under `/<repo>/`, so links and asset paths are relative [practice]; a page with no build step
    needs `.nojekyll` and went live about 20 seconds after each push [T].
19. **Check the live link, not the local copy.** Open the published address at phone and desktop size, take
    screenshots, and use the main path once [T, skill]. A version mark on the page shows that the new release is
    the one being served; load the address with a fresh query string, because the host caches pages for ten minutes
    [T]. If the link is meant to be shared, it has a title, a description and a preview image [R].
20. **A way back.** Tag each release that passed [P1, practice]. To undo one: revert the commit, publish, and check
    the live link again. In our check a rollback command failed silently and only the live check caught it [T].
21. **Once real people's data is in it:** schema changes go through migrations, there is a backup before any
    release that changes stored data and one restore has been tried, test accounts stay out of the live data, and
    a release that changes or deletes live data needs the user's go-ahead. The live site is checked with one
    marked test account that is removed afterwards. Reverting code does not undo a change to data [R, practice].

**At the handoff:**

22. **A note in the README**, for someone who hasn't seen the work [F52]: the live address, how to run it locally,
    how to change it and publish again, how to roll back, where secrets are kept, what is unfinished.

None of the three practitioners described their publish steps or a check of the live address, and Anthropic's
pages cover only who may push or deploy. So stage 3 rests on our one check, the reviewer's gaps and common
practice.

## The finish line and the reply

- **Done when** (large project): every task's check passes; a fresh review against SPEC.md found no correctness
  gap; the live link works at phone and desktop size, with screenshots of the live page; what is live is the
  tagged release; one rollback was tried; the README has the handoff note. The final report lists what was built,
  what was checked and what wasn't, every decision made, and what needs the user [F52, skill].
- **In the reply, not the prompt**, each in a line: the effort level per stage, from `models.md`; what the user
  should have ready before starting (signed in to `gh`, accounts, content); the sentence that starts a later
  session ("Read CLAUDE.md, SPEC.md, TASKS.md and PROGRESS.md, then carry on with the next milestone"); and the
  finish line as a `/goal` line. A small model checks a goal by reading the conversation only, so the condition
  names evidence Claude will print, and ends with a limit sized to the run, a time or a turn count large enough
  for one milestone [CC]. Mention the cheaper build route from `models.md` only for a build that is long but not
  hard, in one sentence, as optional [R].
