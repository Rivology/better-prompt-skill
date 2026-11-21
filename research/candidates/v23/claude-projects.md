# Prompts for work inside a Claude project (2026-11-21)

Read this when the skill runs inside a Claude project, or the prompt will. You can tell because the session has
project tools: a coordinator that starts threads, a progress checklist, decision cards, project memory, a shared
project files folder, and often scheduled tasks, pull request watching, access to the person's computer and
connectors. A plain session has none of these.

A project can do what a single session can't. It runs several threads in parallel, keeps working while the
person is away for hours, wakes itself on a schedule or on a GitHub event, reaches the person's own computer,
and remembers across threads. A strong project prompt uses the parts this task needs, and only those.

## How asking works here

- There is no AskUserQuestion. A choice that is the person's (SKILL.md step 2) goes on a **decision card**: one
  question, 2–4 options, a recommended one. Work that doesn't depend on the answer carries on meanwhile. The step
  that does depend on it waits, if it shapes something the person will rely on (how their data is mapped or merged,
  what gets removed, what is sent) or can't be undone. Other steps go ahead on the recommended option.
- Reversible steps go ahead and get reported: a branch, a pull request, an edit, a query. Irreversible ones wait for
  the person's own word: merging, publishing, deleting, sending a message outside the project, or changing their
  scheduled tasks or settings.

## Project capabilities add to the finish line, never replace it

Keep every check the task needs (totals that reconcile, tests, a fresh reviewer, a rendered check, originals
untouched by checksum) exactly as SKILL.md asks. Threads, schedules and memory decide where and when the work
happens, not whether it gets checked. Each mechanism is concrete: a reminder has a time, a schedule has a cron and a
time zone, and a watch says what event wakes it and what it does then.

## Pick the project capabilities the task needs

| If the task… | Put this in the prompt |
|---|---|
| has parts with separate goals that can run at once | "Split this into threads: [part] and [part], one goal and finish line each. Note which waits on which, and have a thread tell the other when its part is done." In a thread session, this is a request to the coordinator. |
| is a long build or run | "Run it as its own thread", with a progress file and a checklist that shows each step. Follow the project's saved rule on where long runs go (the person's computer, GitHub checks, or the cloud). |
| waits on something outside (a review, CI, an email reply, a deploy) | For a PR: "open it and watch it: fix CI failures and answer review comments as they come". For anything else, concrete reminders: "check [the inbox, the deploy] at [times], and at [deadline] do [next step]". Never wait inside a turn. |
| recurs (daily, weekly) | "Make it a scheduled task" with the schedule in the person's time zone, what each run does, a cap on cost, and where each run reports. |
| needs the person's computer | "Use folder access to read or edit [folder]" for file work. Use "a Remote Control session in [folder]" for running a build, tests, a script or a signed-in tool. Name the folder. |
| needs a web page, or an app on their computer | the built-in browser for sites, and computer use for desktop apps. |
| uses their mail, calendar or files | name the connector, and say that anything sent outside the project waits for a yes on a draft card. |
| produces a document, deck, page or tracker | the deliverable type: a Doc for writing people will keep editing, an Artifact for something to view or use. Attach it to the reply. |
| produces facts later threads will need | "Save [preferences, decisions, where things live] to project memory", one file per subject. Progress stays in the thread. |
| touches private data and a public repo | private data goes in the project files folder or on their computer, never in the repo. |

## What the person sees

- The prompt asks for a checklist that shows real progress. Replies are only for a result, a blocker or a question,
  and each one opens with the outcome or the ask.
- A thread stays open until the work has really ended (a PR merged, a document approved), and resolves then.
- A final report is for someone who was away the whole time: what's done and where, what was checked, and what
  needs them, first.

## Don't

- Spread a small task over threads, schedules or memory. "Rename these files" is one step in one thread.
- Ask the person to babysit: no "tell me when CI finishes" when the thread can watch the PR itself.
- Write instructions for capabilities the project lacks. If a task needs their computer and none is linked, the
  prompt says what to ask for.
