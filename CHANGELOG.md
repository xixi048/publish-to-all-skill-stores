# Changelog

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)；版本号遵循语义化版本。

## [2.1.0] - 2026-10-27

补上「提交到扣子」这件事的**正确答案**。此前只写了「扣子属平台托管、要移植」，
结论对了一半——扣子其实是两队人马，走错队会白做一整轮。

### 新增

- **`references/xiaping.md`** —— 虾评（`xiaping.coze.com`）完整配方：
  - 它是**唯一「Agent 自己注册、自己发布」的技能市场**，官方明说「不支持人工注册」，
    注册即发不设资质门槛，收标准 `SKILL.md` zip（≤10MB，包根放 SKILL.md）
  - 一条 `POST /api/skills`（multipart）就能上架，字段含义与 8 个固定分类
  - **`pledge` 是硬卡点**：版权承诺必须把平台原文照抄给用户、拿到本人明确同意，
    Agent 不得代签；这是本技能里唯一"必须找人"的环节
  - 上传配额按等级：注册送 30 虾米 = A2 = **只有 3 个名额**，动手前先排序
  - 上架默认**试用版**，转正要 20 篇评测 + 加权 ≥4，曝光不靠发布靠评测
  - 六个实测坑，含「返回 Internal server error 但记录已创建 → 重试会白撞配额」、
    「`/api/upload` 自动 +1 版本号」、「安全扫描 502 造成的假风险警报」
- **`store-registry.md`** 增补虾评行，并把扣子技能商店改成申请制事实：
  2026-05 起需专业领域（自媒体/金融/法律/电商/科研/教育/健康医疗）+ 资质证明，
  通用工具类由官方文档自己指向虾评
- **SKILL.md** 渠道分类新增第五类形态「Agent 自注册 API」，并加「扣子技能商店 ≠ 虾评」对照表；
  推送顺序补 3.5 步

### 修正

- 原结论「本机读写类技能在扣子系等于白做」**不适用于虾评** —— 虾评收标准包、不接管运行环境，
  纯本地技能（如全 CG 存档）在那边能正常上架。已在 platform 托管一节加反例说明。

## [2.0.4] - 2026-10-27

- 打包器通用化：`build_wb.py` 从 feeling-search 专用脚本改为任意技能可用的 WorkBuddy 打包器
- 新增 `references/workbuddy-connector.md`：连接器（= MCP 上架通道）四文件结构、远程
  `streamableHttp` 写法、三种认证模式、8 项提交前自检

## [2.0.3] - 2026-10-27

补上此前完全缺位的一家：**WorkBuddy 开放平台**。它是国内抽成最低的付费渠道（内测 1%），
但准入顺序很反直觉，写错顺序会白做一遍。

### 新增

- `paid-channels.md` 增加「一·五、WorkBuddy 开放平台」整节：
  - 三条顺序铁律：先有 1 个过审的**免费**技能才能开收款；观察期只能发 1 个付费资产；
    付费方式（买断/月订）过审后**不可更改**
  - 规格上限：zip ≤3MB、目录**最多两层**、SKILL.md 在包根、头像 512×512
  - **8 个必填字段**：通用规范只有 name + description，这里还要 display_name /
    display_name_en / description_zh / description_en / version / author，缺一解析失败
  - 正确姿势是**打包时注入**而非改源 SKILL.md（否则污染其他商店物料）
  - 完整发布链路，含「付费设置默认是免费、藏在配置步骤里，要手动切」
- `store-registry.md` 把 WorkBuddy 行从「技能目录 △」升级为付费渠道并补提交动作

### 修正

- 付费渠道总表原先只有 skillbay / SkillPay / Coze / 百炼，缺 WorkBuddy，
  导致「能收费的渠道」清单本身不完整

## [2.0.2] - 2026-10-27

把 MCP 这条线的**实测结论**回填，并把「文案」提升为和布局、许可证同级的前置项。

### Changed

- `references/mcp-registries.md`：文案纪律从三条扩到四条，新增「不写会过期的固定数量」
  （`762 words / 598 styles` 这类快照数字会在词库扩充后失真，且已散落在 README、包描述、
  `server.json` 与多个目录站后台，改一次必然漏）
- `SKILL.md`：MCP 章节新增第四条前置约束，并指向 pitfalls 的「文案相关」

### Added

- `references/pitfalls.md`：「文案相关」章节——固定数量的失效链路、正确写法、
  以及已经散到多平台后的补救顺序（先改仓库 → 发新版本让元数据同步 → 无自助编辑入口的站只能重提）

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
