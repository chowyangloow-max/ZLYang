# ZLYang OS

## v1.2 — 目的驱动与随时可调用的能力库

**先判断资料以后用于完成什么任务，再决定调研重点、蒸馏边界、能力卡与调用方法。**

目的充分性而非强制问卷：当用途、未来任务、筛选规则、保留边界、可调用产物范式和成功标准已经明确，就直接做；只缺关键项时，只问一个能改变结果的问题。做知识库本身不是最终用途。

原五模块治理仍在，入口增加 Discovery：

    User task -> Discovery/Purpose Gate -> purpose-selected research
       -> Verify -> Distill -> Baseline (when required) -> Audit -> Knowledge
       -> atomic capability cards -> search index -> task retrieval -> feedback

主要新增文件：

- skills/zlyang-discovery/：目的充分性和调研路由。
- templates/purpose-contract.json：用途契约模板。
- templates/capability-card.json：可检索、带证据与生命周期的能力卡模板。
- docs/purpose-research-recall.md：完整机制、边界与调用范式。
- scripts/purpose_gate.py：真实可运行的 Purpose Gate。
- scripts/build_capability_index.py：卡片结构验证和索引构建。
- scripts/recall.py：按用途、场景、触发词与状态过滤召回。
- scripts/test_purpose_recall.py：独立回归测试。
- workspace/capabilities/：能力卡存储，index.jsonl 是可重建检索索引。

### 本地安装 / 更新

    git clone https://github.com/chowyangloow-max/ZLYang.git
    cd ZLYang
    python3 scripts/init_workspace.py
    python3 scripts/install_codex_skills.py
    python3 scripts/validate.py --records --runs
    python3 scripts/test_purpose_recall.py

已有本地仓库用 git status 检查未提交改动，然后执行 git pull origin main。随后运行 install_codex_skills.py。没有直接访问用户 Mac 文件系统的权限时，远程提交不会自动修改该电脑的本地副本。

### 用途明确时，直接执行而非重复追问

例如给出一段口播稿，并明确用途是内容创作、聚焦前5秒和情绪波峰、近期低粉爆款筛选、尽量保留原文。即刻进入结构分析；没有视频实际数据时标注未经验证，另列可选调研，不把后续卖什么当作强制障碍。

将 templates/purpose-contract.json 复制到 workspace/my-purpose.json 并填入已知信息：

    python3 scripts/purpose_gate.py inspect --file workspace/my-purpose.json

状态 ready 才进入受控正式运行：

    python3 scripts/manage_run.py start --slug content-study --owner operator --objective "短视频能力卡蒸馏" --risk low --purpose-file workspace/my-purpose.json

### 生成与召回可调用知识

能力卡用 JSON 结构保存到 workspace/capabilities/，其中标签、触发短语、未来任务、证据状态、适用范围、前置和例外用于检索和执行边界检查：

    python3 scripts/build_capability_index.py
    python3 scripts/recall.py --purpose 内容创作 --stage 开头 --task "优化前五秒反差开头" --allow-candidate --mode idea

idea 模式可显式包含候选方法并展示警告；execute 模式仅召回 active + verified 的卡，仍须由执行层逐项判断其前置和适用条件。脚本只检索，不直接自动执行。

### 作用和限制

- **不取代原系统**：Verify / Distill / Baseline / Audit / Knowledge 和独立审核、删除账本、覆盖矩阵、反向验证保持存在。
- **分清真实与推测**：点赞、留存等只是已给目标或待核查数据，不能由文本分析推断实际传播效果。
- **按用途调研**：调研路由由 Codex 根据用例和证据缺口执行；脚本本身不自动联网抓取。
- **不是语义搜索**：当前索引为确定性触发词和标签匹配，能复用但对同义改写有局限；未来可加向量召回。
- **不把候选卡当已验证执行能力**：来源可回查、版本可停用，不靠旧规则出现次数判定有效。

完整用法及细节：docs/purpose-research-recall.md 和 docs/run-controls.md。


ZLYang OS 是一个面向 Codex 的信息治理项目。它把海量、混乱、真假参半、互相冲突、版本交错的材料，转成四类真正可用的结果：

- **可信**：每项关键主张都有证据、判定和置信度；
- **可执行**：当前基线明确负责人、步骤、条件、验收与回滚；
- **可追溯**：每个结论都能回溯来源，也能追踪后续替代关系；
- **可维护**：知识资产有复审、保鲜、替代和退役规则。

## 系统架构

```text
Raw inputs
   |
   v
Verify -> Distill -> Baseline -> Audit -> Knowledge
   `-- checkpoints + coverage + deletion + dependencies + review --'
```

## v1.1 控制层

- **运行控制器**：自动建立 run-id、五阶段状态和 Checkpoint，阻止跳关；
- **覆盖矩阵**：跟踪每条承重信息最终进入哪里，暴露遗漏；
- **删除账本**：记录排除、合并、压缩和恢复，承重删减必须复核；
- **依赖图**：检查来源、父记录、版本替代和执行前置是否断链；
- **风险复核**：中风险双路独立验证，高风险再增加独立审计；
- **反向测试**：从基线重建到原始来源，并用删减变异检验承重细节。

总入口 Skill 位于 `skills/zlyang-os/`，下面由五个单一职责模块组成：

- `zlyang-verify`：验证来源、主张、时效和证据；
- `zlyang-distill`：安全去重、压缩，同时保护承重细节；
- `zlyang-baseline`：生成当前唯一执行基线并治理版本；
- `zlyang-audit`：反向检查遗漏、断链和假闭环；
- `zlyang-knowledge`：发布知识并管理复审、替代和退役。

项目还包含一个由 ZLYang 治理的执行能力：

- `generate-openings`：调用用户原有的中文短视频开头方法，生成、诊断、评分并衔接正文。它不是第六个治理阶段；方法升级仍需经过 Verify → Distill → Baseline → Audit → Knowledge。

## 快速开始

1. 初始化或补全工作区。脚本只创建缺失内容，不覆盖已有数据：

   ```bash
   python3 scripts/init_workspace.py
   ```

2. 创建一次受门禁控制的运行：

   ```bash
   python3 scripts/manage_run.py start --slug policy-refresh --owner owner-id --objective "整理当前执行规则" --risk medium
   ```

3. 将原始输入登记到 `workspace/inbox/`，并维护新运行目录中的覆盖矩阵、删除账本、依赖图和复核计划。
4. 完整处理调用总入口 Skill；每阶段完成后使用 `manage_run.py checkpoint` 过关，只处理一个阶段时调用对应模块 Skill。
5. 记录变化后生成依赖图：

   ```bash
   python3 scripts/build_dependency_graph.py --run-id <run-id>
   ```

6. 将机器可读记录放入 `workspace/records/`，然后运行：

   ```bash
   python3 scripts/validate.py --records --runs
   ```

完整控制文件的字段说明见 `docs/run-controls.md`。

## 项目地图

```text
AGENTS.md                 Codex 总操作契约
skills/                   总入口与五个模块 Skill
docs/data-model.md        统一数据模型说明
schemas/                  规范 JSON Schema
templates/                准入与各阶段产物模板
scripts/                  安全初始化与校验脚本
workspace/                实际工作区
```

## 记录标识

记录统一使用 `zly-<type>-<YYYYMMDD>-<slug>-<nn>`，单次运行使用 `run-<YYYYMMDD>-<slug>-<nn>`。ID 一经建立必须保持稳定，文件改名不能改变记录 ID。

## v1.1 边界

v1.1 提供本地文件治理、运行控制、风险复核契约和确定性门禁，不依赖外部服务。多 Agent 复核由 Codex 按 `review-plan.json` 调度并记录，脚本负责验证独立性要求是否满足，但不伪造 Agent 结果。暂不包含数据库、搜索索引、自动抓取、加密签名或工作流界面。
