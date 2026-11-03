# ai-agent-journey

从零开始掌握 AI Agent 的 168 天学习记录。

- 开始日期：2026-11-02
- 计划周期：24 周（Day1 - Day168），结束日 2027-04-17
- 每日投入：工作日约 2 小时，周末约 3 小时
- 环境：Python 3.13.14 / Git 2.56.0 / VS Code

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
- [ ] 记：`notes/Day02.md` 今日笔记（模板在，待补「我踩的坑」）
- [ ] 提交并推送

> 今日按最低标准验收：不用背、不用重写，跑通计算器即算 Day2 通过。
> 类型转换属于「随用随查」的知识，不要求记忆，写到后面自然就熟了。

## 今日复盘（Day1）

- 环境：Python 3.13.14、Git 2.56.0 装好，VS Code 待装。
- 踩坑：建仓库时 GitHub 自动生成了 README，导致本地历史与远端不一致，用 `git push -f` 覆盖解决（仅限空仓库）。
- 学会的命令：`git init`、`git add`、`git commit`、`git remote add`、`git push`、`git status`。
