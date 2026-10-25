# Changelog

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)；版本号遵循语义化版本。

## [2.0.1] - 2026-10-26

把 2.0.0 里"只是列出来"的三类渠道打穿成可执行结论，并补上两个实测会被踩死的坑。

### Added

- **MCP 侧真的落地了**：仓库内置 `mcp/server.py`（stdio / JSON-RPC 2.0 / 零依赖），
  暴露 `skill_store_registry` / `skill_preflight` / `skill_build_package`，README 给了客户端配置
- **自建发现端点已上线**：`docs/.well-known/agent-skills/index.json` 经 GitHub Pages 发布，
  实测 `https://xixi048.github.io/publish-to-all-skill-stores/.well-known/agent-skills/index.json` 返回 200
- **PR 型渠道的政策实测表**：VoltAgent/awesome-agent-skills = `all`（已开 PR #1269）；
  ComposioHQ/awesome-claude-skills = **`collaborators_only`，外部开不了 PR**（1856 个 open issue）

### Fixed

- **GitHub Pages + Jekyll 会跳过点开头的目录**：`.well-known` 必须配一个空的 `docs/.nojekyll`，
  否则文件推上去了但永远 404
- **Official MCP Registry 的真实门槛**：`server.json` 的 `packages[]` 必填
  `registry_type / identifier / version / transport`，即必须先发 npm / PyPI / OCI 包，
  没有包就没有 identifier —— 光有 GitHub 仓库上不了官方 Registry
- **mcp.so**：免费提交要先 Sign In，未登录时表单只给 `$39` 的付费快通道；
  **PulseMCP** 的 `/submit` 会 ERR_ABORTED 跳到内容页；**cursor.directory** 有 429 人机校验

### Changed

- 国内第二批（Kimi Claw / 小红书 Red Skill / 美团虾345 / WorkBuddy）逐个查了入口：
  **均无法确认存在公开的技能商店提交入口**，继续以 △ 标注，不写进可执行清单

## [2.0.0] - 2026-10-26

第二版：把「经验」升级成「可执行的渠道全景 + 判定方法」，并把渠道表从 24 扩到 36。

### Added

- **渠道全景扩到 36 个**，新增三类此前整块漏掉的：
  - 真·技能市场：LobeHub Skills
  - CLI / 注册中心：agentskills.in、讯飞 Astron SkillHub（`skill.xfyun.cn`，有发布页）
  - MCP 侧目录群：Official MCP Registry / Smithery / Glama / mcp.so / PulseMCP / Cursor Directory
  - 官方与社区列表：anthropics/skills、Claude Connectors Directory、5 个 awesome 列表
  - 国内第二批：Kimi Claw、小红书 Red Skill、美团 虾345、WorkBuddy 技能中心
  - 自建发现端点 `/.well-known/agent-skills/index.json`
- SKILL.md 增加「每轮先扫一遍市场」的具体命令与**假表单判据**（提交后必须有回执 id 或 PR）
- 付费机制实测结论：**能否收费取决于形态而非渠道**
  - 腾讯 SkillPay：平台暂不收技术服务费（0 抽成）、按次计费、支付宝/微信实时结算，
    但只认「依赖后端、脱离后端无法独立运行」的 Pay Skill —— 纯本地脚本型技能转不了
  - 阿里云百炼：AI 打赏 + Agent Commerce 统一分账，需服务商/ISV 身份，同样要求可调用服务

### Changed

- 渠道表加入「形态（api / pr / cli / form / auto / tool / port）」与「是否可收费」两列，
  `submit_all.py --registry` 一条命令打印全表
- 发布前铁律更新：**先上 GitHub，默认私有，但必须先问用户要不要开源**，
  并说明代价（私有 → 自动索引型渠道全部失效）
- 语言约定：**英文区用英文，中文区用中文**（frontmatter 保持英文，本地化只在商店展示字段）

### Fixed

- `preflight.py` 的仓库根推断改为向上找 `.git`（原先用 `skill_dir.parent`，
  在 `skills/<name>/` 布局下会误报"缺少 LICENSE"）

## [1.0.0] - 2026-10-26

- 初版：五类提交形态、24 个渠道、上架体检器、打包器、批量提交器
