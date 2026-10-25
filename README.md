# skill-store-publisher

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> An agent skill for pushing an existing `SKILL.md` skill to agent-skill marketplaces — at home and abroad,
> free and paid — without wasting a week rediscovering how each one actually accepts a submission.

**中文说明见下。**

## What it is

A playbook, not a wrapper. It tells an agent how each class of store actually works, so no time is wasted
on the ones that will never accept a file drop:

| Form | Submission action | Examples |
|---|---|---|
| Auto-indexed from GitHub | fix the repo (path + topics + README) | skills.sh, SkillsMP, claude-plugins.dev |
| Public submit API | one HTTP POST | skillstore.io, skillsmd.dev, skillbay.sh |
| GitHub PR | fork → add file → PR | buildwithclaude, awesome lists |
| Login-gated CLI / OAuth form | log in first | ClawHub, Tank, Cow Skill Hub, agentskill.sh |
| Platform-hosted | **port the skill** — a different project | Coze, AgentMore, GPT Store |

## Install

```bash
npx skills add xixi048/skill-store-publisher
```

```text
/plugin marketplace add xixi048/skill-store-publisher
```

## What's inside

```
skills/skill-store-publisher/
├── SKILL.md                       the decision-first workflow
├── references/
│   ├── store-registry.md          24 channels: region, pricing, form, verification level
│   ├── submission-recipes.md      6 recipes + SPA recon + mirror/token push
│   ├── paid-channels.md           revenue splits, skillbay field table, price tiers
│   └── pitfalls.md                20+ "symptom → cause → fix" entries
└── scripts/
    ├── preflight.py               readiness check (layout, license, danger calls, network)
    ├── build_package.py           build the shapes each store wants
    └── submit_all.py              batch submitter (--registry for the full table)
```

## Quick start

```bash
# 1. readiness check — ERROR means don't submit yet
python skills/skill-store-publisher/scripts/preflight.py <repo>/skills/<name>

# 2. build the package shapes
python skills/skill-store-publisher/scripts/build_package.py <repo> skills/<name> --out dist

# 3. see every channel and its submission form
python skills/skill-store-publisher/scripts/submit_all.py --registry

# 4. batch submit the ones that need no login
python skills/skill-store-publisher/scripts/submit_all.py --all --repo <github-url>
```

## The one rule that pays for itself

Directory sites only index `skills/<name>/SKILL.md`. A skill sitting at the repo root is **never discovered
and never errors** — it simply stays invisible. Move it, fix the relative paths, re-submit.

## Requirements

Python 3.8+, standard library only. No network calls from the scripts except the public endpoints you ask for.

## License

MIT — see [LICENSE](LICENSE).
