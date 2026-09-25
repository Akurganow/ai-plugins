---
name: interests
description: >
  Interview a person about what they follow and write the measurable
  questions their forecast is built on. Ask one question at a time, turn
  each interest into dated, checkable questions, and write interests.yaml
  and questions/<interest>.yaml once the user approves them. Use when the
  user wants to choose what to track or forecast, or to turn an interest
  into questions. Also use when they want to add or change an interest or a
  question, or reword a question no market covers. Also use to start a
  forecast workspace from nothing.
license: MIT
---

# Interests into measurable questions

The `forecast` skill binds questions to prediction markets and records their
probabilities. The questions come from here. This skill interviews the
person and writes the two files they own: `interests.yaml` and
`questions/<interest>.yaml`.

Read `references/interview.md` before the first question. It holds the
interview, both file formats, what makes a good question and the rules for
writing the files.

## Where the files go

The files go in the forecast workspace, the directory every `hp` command
takes as `--repo`. Its layout is in `../forecast/SKILL.md`, section "The
workspace". When no workspace exists yet, ask the user where it should go.

Read `../forecast/references/procedures.md` before you settle a question's
`horizon` with the user. Its section 1 holds the horizon convention, which
decides the verdict a market can earn against that date.

## Afterwards

Hand over to the `forecast` skill once you have written the files. It gets
`hp`, checks the files with `hp ingest check questions`, and binds each
question to a market. This skill runs no binary: it talks with the person and writes
YAML.
