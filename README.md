# ZLYang OS

**先搞清资料以后用来做什么，再决定调研、蒸馏、保存和调用什么。**

ZLYang OS 是面向 **Codex** 的目的驱动信息处理与可复用能力系统。它不追求“整理出更多文档”，而是把原始资料转成以后**找得到、用得上、可验证、可追溯、能更新**的知识和方法。

> **关键规则：用途、规则、边界与输出范式已经明确，就直接做；只有缺少会改变结果的关键信息才追问。**

## 1. 安装（Mac / Linux）

需要预先安装 [Git](https://git-scm.com/) 、**Python 3.10+** 和 Codex。

打开终端，复制这一行即可：

```bash
git clone https://github.com/chowyangloow-max/ZLYang.git && cd ZLYang && python3 scripts/setup.py
```

**这一条命令自动完成：** 下载项目、初始化工作区、把 Skills 注册到项目内的 `.agents/skills/`、检查目录和运行基础测试。不删除或覆盖已有工作数据。

然后在 **Codex 中打开 `ZLYang` 文件夹**，输入：

```text
使用 $zlyang-os，分析我提供的资料。
先判断用途是否明确：明确就直接做；缺关键信息才问。
按实际用途蒸馏，保护关键细节，生成今后可检索调用的能力卡。
```

> 这是**项目级安装**，在该项目中打开 Codex 才会自动发现对应 Skills；若未出现，重新打开 Codex 项目。

**已经安装，如何更新？** 在原来 `ZLYang` 目录运行：

```bash
git pull origin main && python3 scripts/setup.py
```

更新前可先运行 `git status`，如果显示未提交的本地改动，先保存或处理，避免拉取冲突。

## 2. 它解决哪些问题？

| 遇到的问题 | ZLYang OS 的做法 |
| --- | --- |
| 文档整理了一堆，却不知道以后怎么用 | 先确认未来实际任务，定向蒸馏 |
| 已经说清用途，AI 还一直追问 | 用途充分性检查：够用就开始 |
| 压缩后丢了前置、例外、顺序、关键细节 | 覆盖矩阵、删除账本、依赖图、反向审计 |
| 历史规则废弃了，还被重复执行 | 生命周期与版本替代、当前执行基线 |
| 以前总结过的方法找不到 | 能力卡 + 用途/标签/触发词索引 |
| 观点或作者自述被当作事实 | 来源核验、证据状态、候选与已验证分离 |

## 3. 三个实际使用例子

**例 A：短视频文案分析**

你交一篇逐字稿，说：“拿来研究选题、前五秒、情绪波峰、口播结构，原稿尽量别改。”

系统识别目的已经足够，不重复问“你要卖什么”；提取开头、结构、节奏和可复用方法，记录来源与限制。没有真实视频数据时，只能标注传播效果为**待验证判断**。

**例 B：整改文件 / 项目 SOP**

输入旧方案、新决策、复盘和操作手册，目的为“给执行人唯一当前正确清单”。系统区分当前有效、已替代和冲突内容；保留前置条件、分支、异常、验收，再生成执行基线。

**例 C：做长期知识库**

“我要做知识库”只说明**存储形式**，没有说明未来调用任务。此时系统会优先确认：“以后你要用这套资料做什么？” 确定用途后，才决定怎么提取与标记。

## 4. 工作流程

```text
用户任务与材料
    ↓
Discovery：确认用途充分性（够用直接做，不够只问关键点）
    ↓
按用途选定调研方向、保留重点和验收标准
    ↓
Verify → Distill → Baseline* → Audit → Knowledge
    ↓
原子能力卡（触发条件 / 方法 / 来源 / 标签 / 使用边界 / 状态）
    ↓
索引检索 → 任务匹配 → 核对适用条件 → 调用 → 结果反馈

* Baseline 专门处理需要唯一当前执行规则的任务；
  内容创作分析可先输出清楚标注为候选的机制卡。
```

| 模块 | 职责 |
| --- | --- |
| **Discovery** | 识别目的、定向调研、只问关键问题 |
| **Verify** | 事实、来源、时效、冲突证据 |
| **Distill** | 目的导向提炼、保留承重细节 |
| **Baseline** | 有效版本、执行步骤、替代关系 |
| **Audit** | 覆盖、遗漏、断链、反向验证 |
| **Knowledge** | 能力卡、标签、召回、复审退役 |

仓库额外包含 `generate-openings`：中文短视频开头生成与诊断 Skill，它是业务能力，不是治理阶段。

## 5. 目录说明

```text
ZLYang/
├── AGENTS.md                   Codex 项目约束
├── README.md                   入口说明
├── skills/
│   ├── zlyang-os/              统一入口
│   ├── zlyang-discovery/       用途识别
│   ├── zlyang-verify/          核验
│   ├── zlyang-distill/         蒸馏
│   ├── zlyang-baseline/        当前执行基线
│   ├── zlyang-audit/           保真审计
│   ├── zlyang-knowledge/       知识发布
│   └── generate-openings/      短视频开头
├── templates/                  目的契约、能力卡、阶段模板
├── docs/                       详细机制和数据模型
├── scripts/                    安装、校验、索引、运行
└── workspace/
    ├── inbox/                  原始材料
    ├── capabilities/           可调用能力卡
    ├── evidence/               证据/来源
    ├── records/                可追溯记录
    ├── baselines/              当前执行规则
    ├── audits/                 审计
    ├── knowledge/              发布知识
    ├── runs/                   检查点和运行日志
    └── archive/                历史归档
```

## 6. 需要时才用的进阶命令

平时用自然语言在 Codex 中描述任务即可；只有调试或批量运行才需要以下命令。

**检查用途契约：**

```bash
python3 scripts/purpose_gate.py inspect --file workspace/my-purpose.json
```

**建立能力卡索引并检索：**

```bash
python3 scripts/build_capability_index.py
python3 scripts/recall.py --purpose 内容创作 --stage 开头 --task "优化前五秒反差开头" --allow-candidate --mode idea
```

**检查项目：**

```bash
python3 scripts/validate.py --records --runs
python3 scripts/test_purpose_recall.py
```

详细说明：[目的、调研与召回机制](docs/purpose-research-recall.md) · [运行控制](docs/run-controls.md) · [统一数据模型](docs/data-model.md)

## 7. 当前能力边界

- 已有**目的充分性检查、受控流程、可检索的结构化能力卡和关键词召回**；目前尚不是向量语义检索。
- 定向调研由有相应工具的 Codex 执行，本地脚本不自动联网。
- 点赞、留存等目标值不能凭文案直接推断为已证实结果。
- 候选卡可辅助创作，但**未经验证的卡不允许自动执行**。
- 安装脚本只处理当前项目，不负责更改用户电脑上的其他文件夹。

---

**ZLYang OS 的目标不是整理得更漂亮，而是在下一个具体任务出现时，让正确的信息能被准确找到并使用。**
