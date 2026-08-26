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
   `--------- unified records + lineage + run manifest ---------'
```

总入口 Skill 位于 `skills/zlyang-os/`，下面由五个单一职责模块组成：

- `zlyang-verify`：验证来源、主张、时效和证据；
- `zlyang-distill`：安全去重、压缩，同时保护承重细节；
- `zlyang-baseline`：生成当前唯一执行基线并治理版本；
- `zlyang-audit`：反向检查遗漏、断链和假闭环；
- `zlyang-knowledge`：发布知识并管理复审、替代和退役。

## 快速开始

1. 初始化或补全工作区。脚本只创建缺失内容，不覆盖已有数据：

   ```bash
   python3 scripts/init_workspace.py
   ```

2. 把 `templates/intake.md` 复制到新的运行目录，并将原始输入登记到 `workspace/inbox/`。
3. 完整处理调用总入口 Skill；只处理一个阶段时，调用对应模块 Skill。
4. 将机器可读记录放入 `workspace/records/`，然后运行：

   ```bash
   python3 scripts/validate.py
   ```

5. 使用 `python3 scripts/validate.py --records` 进一步检查工作区中的 JSON 记录。

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

## 第一版边界

第一版提供本地文件治理和确定性校验，不依赖外部服务。暂不包含数据库、搜索索引、自动抓取、加密签名或工作流界面；这些能力应在真实运行暴露出稳定边界后再增加。
