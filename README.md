# ai-agent-journey

从零开始掌握 AI Agent 的 168 天学习记录。

- 开始日期：2026-11-02
- 计划周期：24 周（Day1 - Day168），**2026-11-10 重排后结束日 2027-04-22**
- 每日投入：工作日 30~45 分钟（只做「必做」），周末 1~2 小时
- 环境：Python 3.13.14 / Git 2.56.0 / VS Code

## 知识总览（忘了就查这里）

- **`notes/day01_05_overview.md`** —— Day1~Day5 全部知识点 + 每个点一个能跑的例子 + 10 题自测
- **`python code/recap_day1_5.py`** —— 一条命令跑完全部例子，亲眼看输出

## 当前排期（2026-11-10 重排）

真实进度：Day1~Day5 已完成并推送。Day6 起按下面这张表走。

| 日期 | Day | 主题 | 必做（30~45 分钟） |
|---|---|---|---|
| 11-10 二 | Day5 | 函数与模块化 | ✅ 已完成（`7105850`）|
| 11-11 三 | Day6 | 文件 / JSON / 路径 | 跑 `day06_todo.py`，add→list→done 各一次，关终端再开确认数据还在 |
| 11-12 四 | Day7 | 周复盘 | 填 `notes/Week01-review.md` 前四节 + 写 300 字周记 |
| 11-13 五 | Day8 | 面向对象 | 用 dataclass 定义 `Message(role, content)` 和 `ToolCall(name, args)` |
| 11-14 六 | Day9 | 类型注解与 Pydantic | 定义 Tool 参数模型，故意传错类型看它报什么错 |
| 11-15 日 | Day10 | 异步编程 asyncio | 串行请求 5 次 vs `asyncio.gather` 并发，记录耗时差 |

**三条节奏规则（比进度更重要）**

1. 工作日只做「必做」，30~45 分钟。没做完就顺延，**绝不一天补两格**。
2. 周末多做了是赚的（提前），不是义务。
3. 中断超过 3 天，回来第一件事是打开计划页点「按当前进度对齐到今天」，然后从那天继续，不看日历发愁。

## 规则（写给自己）

1. 每天的代码和笔记必须进这个仓库，不留本地孤儿文件。
2. 不写评测就不许改 prompt。
3. 每个阶段结束，产出一篇公开文章或一个可运行项目。

## 目录结构

```
notes/     每天的学习笔记（Day01.md ... Day168.md）
code/      每天的代码
reports/   实验报告与评测数据
docs/      项目立项文档
```

## 阶段进度

| 阶段 | 周次 | 内容 | 状态 |
|---|---|---|---|
| P1 | W1-4 | Python / Prompt / Function Calling | 进行中 |
| P2 | W5-6 | RAG 检索增强 | 未开始 |
| P3 | W7-11 | Agent 内核（手写 ReAct、自研框架） | 未开始 |
| P4 | W12-14 | LangGraph / Agents SDK / CrewAI | 未开始 |
| P5 | W15-17 | 记忆 / 上下文工程 / MCP / A2A | 未开始 |
| P6 | W18-20 | 评测 / 可观测 / 部署 / 安全 | 未开始 |
| P7 | W21-24 | 三个实战项目 + 作品集 | 未开始 |

## Day1

- [x] 安装 Python 3.13.14
- [x] 安装 Git 2.56.0，配置用户名与邮箱
- [x] 安装 VS Code（待装 Python 插件）
- [x] 创建本仓库并写清学习目标
- [x] 创建虚拟环境 `.venv`（`python -m venv .venv`）
- [x] 跑通 `code/day01_hello.py`
- [x] 推送到 GitHub（commit dfd6388）

## Day2 · Python 基础语法（2026-11-03 完成）

- [x] 学：变量与赋值、四种基本数据类型（int / float / str / bool）
- [x] 学：运算符、字符串格式化（f-string）
- [x] 学：input() / print() / type()
- [x] 写并跑通：`code/day02_calculator.py`（输入 10 和 3，四行结果正常）
- [x] 补：`notes/python_type_conversion_cheatsheet.md` 类型转换速查卡
- [x] 记：`notes/Day02.md` 今日笔记（2026-11-08 补齐「我踩的坑」与总结）
- [x] 提交并推送（2026-11-04 确认，origin/main = e06ab08）

> 今日按最低标准验收：不用背、不用重写，跑通计算器即算 Day2 通过。
> 类型转换属于「随用随查」的知识，不要求记忆，写到后面自然就熟了。

## Day3 · 数据结构：列表 / 字典 / 元组 / 集合（2026-11-04）

- [x] 学：5.1 列表（索引、切片、append / remove、遍历）— 2026-11-04
- [x] 学：5.5 字典（get / items / 键值遍历）— 2026-11-05
- [x] 学：列表推导式、字典推导式（练习 `code/day03_comprehension.py` 三项全过，速查 `notes/python_comprehension_cheatsheet.md`）
- [x] 写并跑通：`code/day03_wordcount.py`（读 `code/sample.txt`，输出词频 Top 20）
- [x] 改一处并跑通：用 `code/day02_calculator.py` 当输入跑通（71 词 / 45 unique）
- [x] 记：`notes/Day03.md`（2026-11-08）
- [x] 提交并推送（与 Day4 合并为 a2c74a0）

> 目标是「会用」不是「背下来」。忘记语法就翻 `notes/Day03.md`，那里面有一张速查表。
> 唯一值得记住的一行：`counts[w] = counts.get(w, 0) + 1`

## Day4 · 控制流与异常处理（2026-11-05）

- [x] 学：if / elif / else、for / while、break / continue
- [x] 学：try / except / else / finally，认识常见异常类型（官方 8.3 / 8.7）
- [x] 写并跑通：`code/day04_guess.py`（猜数字，非法输入不崩、不扣次数）
- [x] 改一处：`MAX_TRIES` 8 → 3，实测开局提示变「3 次机会」
- [x] 读：`notes/Day04.md` 第四节「为什么 Agent 必须捕获工具异常」（2026-11-08）
- [x] 记：`notes/Day04.md`（2026-11-08）
- [x] 提交并推送（与 Day3 合并为 a2c74a0）

> 今天唯一要带走的：**别让程序因为一行坏输入就崩，也别让 Agent 因为一次工具失败就死。**

## Day5 · 函数与模块化（2026-11-10 完成）

- [x] 学：def / 参数 / 返回值 / 默认参数（速查 `notes/python_function_cheatsheet.md`）
- [x] 学：*args / **kwargs / lambda / 作用域（只要求「见过」，会看即可）
- [x] 跑通：`code/day05_functions.py`（七种写法对照）
- [x] 重构：`code/day02_calculator_func.py` 拆成 4 个函数 + main()，`day05_verify.py` 三组输入逐字节一致
- [x] 小实验：`code/day05_quiz_demo.py`（给 calculate 加 `//`，证明 print_results 不用改）
- [x] 记：`notes/Day05.md`
- [x] 提交并推送（`7105850`）

> 今天的验收线只有一条：**输入 10 和 3，重构版的输出必须和原来完全一样。**
> 工具（tool）就是函数 —— 你现在写的每个函数，都是 Day40 之后 Function Calling 的零件。

## Day6 · 文件、JSON、路径（2026-11-07，待补）

- [ ] 学：`open()` / `read_text` / `write_text`、`encoding="utf-8"` 为什么必须写
- [ ] 学：`json.loads` / `json.dumps`、`ensure_ascii=False` 的作用
- [ ] 学：`pathlib.Path`、`Path(__file__).parent` 为什么比相对路径可靠
- [ ] 跑通：`code/day06_todo.py list`（空清单不报错）
- [ ] 用一遍：`add` / `list` / `done` / `rm` 各一次，关掉终端再开，数据还在
- [ ] 记：`notes/Day06.md`
- [ ] 提交并推送

> 验收：**关掉 PowerShell 再打开，`list` 出来的条目还在。**
> JSON 是你和大模型沟通的通用语言 —— 后面每一次工具调用、每一条对话历史，都是 JSON。

## Day7 · 周复盘 + 第一次用 AI 写代码（2026-11-08）

- [ ] 复盘：把 Day1~Day6 的打卡项逐条过一遍，没勾的今天补齐或明确划掉
- [ ] 确认：本地与远端一致（`git status -sb` 显示 `## main...origin/main` 且无改动）
- [ ] 写：`notes/Week01-review.md`（学了什么 / 卡在哪 / 下周改什么）
- [ ] 试：用 AI 帮你写一个小工具（比如把 `day03_wordcount.py` 改成支持中文分词），体验「说需求 → 改代码 → 验收」
- [ ] 提交并推送

> 周复盘的作用不是打卡，是**发现自己哪一天在假装学习**。写不出来，就是没学会。

## 今日复盘（Day1）

- 环境：Python 3.13.14、Git 2.56.0 装好，VS Code 待装。
- 踩坑：建仓库时 GitHub 自动生成了 README，导致本地历史与远端不一致，用 `git push -f` 覆盖解决（仅限空仓库）。
- 学会的命令：`git init`、`git add`、`git commit`、`git remote add`、`git push`、`git status`。
