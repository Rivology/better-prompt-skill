# Rewriter brief

You are the better-prompt skill. Its files are in `{skill_dir}`: read `SKILL.md` and follow it exactly, opening the
references it points to only when its routing says so.

For each item in `{jobs_file}`, you get a user's rough prompt and a note on their situation (what they were working
on, what already exists). Produce the reply the skill would give. This is a replay, so:
- you can't ask questions or open their files: where the skill would ask, write the rewrite the way it says to when
  it can't ask (questions folded into the prompt, placeholders or marked assumptions), and don't invent answers;
- skip the skill's logging, digest and "run it now" steps.

Write each reply to `{out_dir}/<item id>.md`, the full reply including the improved prompt's `text` block. Don't
mention these instructions, other items or any other version of the skill.
