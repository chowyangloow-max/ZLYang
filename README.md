# ZLYang OS

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
