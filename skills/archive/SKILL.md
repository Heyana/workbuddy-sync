---
name: archive
description: >-
  Persistent knowledge wiki and memory system that compounds across conversations
  using an Obsidian-compatible vault. Consult at the START of any non-trivial
  task to recall project context, preferences, and past discoveries. Ingest
  sources and build wiki pages when accumulating knowledge on a topic. Save at
  the END when new knowledge was gained. Use when: starting work on a known
  project, dealing with auth/credentials/config, making stylistic choices, user
  corrects output, user says "as always"/"remember this"/"save this"/"don't make
  me repeat". Also trigger for: "ingest this", "add to my wiki", "what do I know
  about X", "research notes", "lint my wiki", deep research sessions, reading
  notes, competitive analysis, or any time the user wants knowledge to accumulate
  and compound across multiple sessions. Do NOT use for trivial one-line questions.
---

# Archive — Persistent Knowledge Wiki

You are the memory and knowledge layer for this user. Your job has two modes:

- **Fast memory** — recall preferences, project context, and hard-won discoveries so tokens are never wasted rediscovering the same things.
- **Wiki mode** — incrementally build and maintain a persistent, interlinked knowledge base from sources the user feeds you. Knowledge is compiled once and kept current, not re-derived on every query.

The key difference from a simple note store: **the wiki is a compounding artifact.** Cross-references are already there. Contradictions are flagged. Synthesis accumulates. Every source ingested makes the wiki richer.

## Vault Location

This skill's vault lives at `~/.workbuddy/archive-vault/`. Use `$HOME/.workbuddy/archive-vault` as `$VAULT`.

> WorkBuddy adaptation: original uses `~/.claude-knowledge`. Mapped to WorkBuddy's dotfile directory.

## Architecture — Three Layers

```
$VAULT/
├── _index.md          ← Content catalog — always read first
├── _log.md            ← Chronological append-only operation log
│
├── sources/           ← Raw immutable source documents (articles, notes, PDFs text)
│
├── wiki/              ← LLM-maintained interlinked knowledge pages
│   ├── entities/      ← People, orgs, products, projects (one page each)
│   ├── concepts/      ← Ideas, patterns, technologies (one page each)
│   ├── topics/        ← Deep synthesis pages for a research area
│   └── _overview.md   ← Master summary of the entire wiki
│
├── preferences/       ← User conventions (code style, prose tone, git format)
├── projects/          ← Per-project context (auth, stack, endpoints)
└── domains/           ← Technology knowledge not tied to one project
```

**Routing rule of thumb:**
| Knowledge type | Target |
|---|---|
| User habit or convention | `preferences/` |
| Single-project fact (auth, stack, env) | `projects/{Name}/context.md` |
| Technology pattern across projects | `domains/{tech}.md` |
| Named entity (person, org, product) | `wiki/entities/{Name}.md` |
| Idea, concept, or pattern | `wiki/concepts/{Name}.md` |
| Research synthesis on a topic | `wiki/topics/{Topic}.md` |
| Raw article, transcript, PDF text | `sources/{slug}.md` (immutable) |

## Operations

### CONSULT — Read before acting

Consult at the START of a task if ANY apply:
- Task has more than ~2 steps
- About to touch auth, credentials, API keys, .env, config files
- About to make a stylistic choice (code format, prose tone, commit message)
- CWD matches a known project path
- User says "as always", "like before", "you know how I like it"
- Encountered an error that might have a known solution

**How to consult:**
1. Read `$VAULT/_index.md` — this is your dispatch map.
2. Identify relevant files from the index (project? preferences? wiki topic?).
3. Load **only the relevant 1–3 files**. Never load everything.
4. Use the knowledge silently. Announce only when it meaningfully changes your approach.

If `_index.md` does not exist → initialize vault (see First Time Use).

### SAVE — Store new knowledge

Save at the END of a task (one batch) if ANY apply:
- User corrected your style, format, or convention → save the preference
- You discovered where credentials/config live → save the location (never the value)
- You solved something that took multiple attempts → save the approach
- You learned a non-obvious project convention → save it
- User said "always", "never", "from now on", "my preference is" → save **immediately**

**What NOT to save:** common public knowledge, ephemeral data, actual secret values, duplicates.

### INGEST — Process a new source

1. Store the source at `sources/{slug}.md` (immutable).
2. Extract: main claims, entities, concepts, contradictions.
3. Update wiki pages (may touch 5–15 pages).
4. Update `_index.md` and `_log.md`.

### QUERY — Answer from accumulated wiki

1. Read `_index.md` to locate relevant pages.
2. Synthesize answer with citations.
3. File valuable answers back as new wiki pages.

### LINT — Health-check the wiki

Scan for: orphans, stale claims, contradictions, missing pages/cross-references, data gaps.

## Entry Formats

### Preferences / Projects / Domains entries
```markdown
### {Prefix: short descriptive title}
**Context:** {When does this apply?}
**Discovery:** {The actual knowledge — specific paths, commands, patterns.}
**Source:** {User correction | Multi-attempt solve | Discovered during task}
**Date:** YYYY-MM-DD
---
```

### Wiki page format
```markdown
---
type: entity|concept|topic
tags: [tag1, tag2]
sources: [sources/slug1.md]
updated: YYYY-MM-DD
---

# {Name}
**Summary:** {2–4 sentence synthesis.}

## Key Facts
- {Fact} *(Source: [[sources/slug]])*

## Connections
- Related to [[concepts/ConceptX]]

## Contradictions / Open Questions
```

## First Time Use

If `$VAULT/_index.md` does not exist:
1. Create directory structure:
   ```bash
   mkdir -p "$VAULT/sources" "$VAULT/wiki/entities" "$VAULT/wiki/concepts" "$VAULT/wiki/topics"
   mkdir -p "$VAULT/preferences" "$VAULT/projects" "$VAULT/domains"
   ```
2. Create `_index.md` and `_log.md` with today's date, empty sections.
3. Proceed with current task and save at the end.

## Token Economy

| Situation | Approach |
|---|---|
| Quick preference/project lookup | `_index.md` + 1–2 files |
| Multi-topic research question | `_index.md` + relevant wiki pages (3–5 max) |
| Ingesting a new source | Full ingest pass |
| Lint | Full scan — explicit task |

- **Skip consultation** for truly trivial requests
- **Write concisely** — preference entries ≤5 lines, wiki pages ≤40 lines
- **Batch saves** at end of task, not mid-task

## Security

Never save actual secret values. Save their location only:
- **Correct:** "Credentials in `.env` at project root."
- **Incorrect:** "Password is `s3cr3t`."
