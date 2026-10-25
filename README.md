# publish-to-all-skill-stores

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 同时上架所有 Skill 商店 · an agent skill for pushing an existing `SKILL.md` skill to agent-skill marketplaces — at home and abroad,
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

## What's new in v2

- channel registry 24 → **36** (adds LobeHub, agentskills.in, XFYUN Astron, the MCP-side directories, official repos, the CN second tier, and the `/.well-known/agent-skills/index.json` discovery endpoint)
- a named rule for whether a store is real: **no receipt id and no PR means it did not happen**
- paid research: **payment depends on form, not on channel** — Tencent SkillPay is 0-cut but only accepts backend-backed "Pay Skill"

## Install

```bash
npx skills add xixi048/publish-to-all-skill-stores
```

```text
/plugin marketplace add xixi048/publish-to-all-skill-stores
```

## What's inside

```
skills/publish-to-all-skill-stores/
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
python skills/publish-to-all-skill-stores/scripts/preflight.py <repo>/skills/<name>

# 2. build the package shapes
python skills/publish-to-all-skill-stores/scripts/build_package.py <repo> skills/<name> --out dist

# 3. see every channel and its submission form
python skills/publish-to-all-skill-stores/scripts/submit_all.py --registry

# 4. batch submit the ones that need no login
python skills/publish-to-all-skill-stores/scripts/submit_all.py --all --repo <github-url>
```

## The one rule that pays for itself

Directory sites only index `skills/<name>/SKILL.md`. A skill sitting at the repo root is **never discovered
and never errors** — it simply stays invisible. Move it, fix the relative paths, re-submit.

## Use as an MCP server

The same three tools are exposed over MCP (stdio, zero dependencies), so any MCP-capable agent can
call them directly:

```json
{
  "mcpServers": {
    "publish-to-all-skill-stores": {
      "command": "python",
      "args": ["C:/path/to/publish-to-all-skill-stores/mcp/server.py"]
    }
  }
}
```

Tools: `skill_store_registry` (36 channels), `skill_preflight` (readiness check),
`skill_build_package` (zip shape stores ask for).

## Machine-discoverable index

`docs/.well-known/agent-skills/index.json` is published on GitHub Pages so agents that honour the
`/.well-known/agent-skills/index.json` convention can find these skills without any store:

```text
https://xixi048.github.io/publish-to-all-skill-stores/.well-known/agent-skills/index.json
```

## Requirements

Python 3.8+, standard library only. No network calls from the scripts except the public endpoints you ask for.

## License

MIT — see [LICENSE](LICENSE).
