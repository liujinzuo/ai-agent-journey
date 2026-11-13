"""Day7 巩固测验：Day2 ~ Day6 知识点，共 12 题。

用法：
    python code/day07_quiz.py

输入 A / B / C / D 作答，每题答完立刻给对错和解析。
随时输入 q 退出。
"""

LINE = "-" * 62

QUESTIONS = [
    {
        "topic": "Day2 · input() 返回字符串",
        "code": """
a = input("请输入一个数：")

print(a + 3)
""",
        "q": "运行后在提示处输入 10，会发生什么？",
        "options": [
            "A. 输出 13",
            "B. 报 TypeError",
            "C. 输出 103",
            'D. 输出 "103"',
        ],
        "answer": "B",
        "why": "input() 读到的永远是字符串 \"10\"。字符串 + 整数在 Python 里不允许，"
               "直接抛 TypeError。想算数必须先 float() 或 int() 转。\n"
               "        注意区分：\"10\" + \"3\"（两个都是字符串）才会拼接成 \"103\"。",
    },
    {
        "topic": "Day3 · 字典计数",
        "code": None,
        "q": "字典 counts 里现在还没有 \"agent\" 这个键。要把它记成出现 1 次，哪句是对的？",
        "options": [
            'A. counts["agent"] = counts["agent"] + 1',
            'B. counts["agent"] = counts.get("agent", 0) + 1',
            'C. counts.append("agent")',
            'D. counts["agent"] += 1',
        ],
        "answer": "B",
        "why": 'A 和 D 在键不存在时会抛 KeyError —— 取不到值，就没法加。'
               'get("agent", 0) 的意思是「取不到就给个默认值 0」，然后再 +1 写回去。'
               "这一行是 Python 里计数的万能写法。",
    },
    {
        "topic": "Day3 · 列表推导式",
        "code": """
nums = [1, 2, 3, 4]
result = [n * 2 for n in nums if n > 2]
print(result)
""",
        "q": "输出是什么？",
        "options": [
            "A. [2, 4, 6, 8]",
            "B. [6, 8]",
            "C. [3, 4]",
            "D. [2, 4]",
        ],
        "answer": "B",
        "why": "读法：[产出 for 来源 if 条件]。先按 if 筛出 3 和 4，再各自乘 2，得 [6, 8]。\n"
               "        if 写在 for 后面 = 过滤，结果数量会变少。",
    },
    {
        "topic": "Day5 · return vs print",
        "code": """
def show(msg):
    print(f"打印：{msg}")

result = show("你好")
print(f"返回值：{result}")
""",
        "q": "输出是什么？",
        "options": [
            "A. 打印：你好 / 返回值：打印：你好",
            "B. 打印：你好 / 返回值：你好",
            "C. 打印：你好 / 返回值：None",
            "D. 报错",
        ],
        "answer": "C",
        "why": "show() 里只有 print，没有 return，所以它交出去的东西是 None。"
               "屏幕上那行字是 print 的副作用，程序拿不到。\n"
               "        判断一个函数有没有交出结果，只看有没有 return。",
    },
    {
        "topic": "Day4 · break vs continue",
        "code": None,
        "q": "for 循环里 break 和 continue 的区别是什么？",
        "options": [
            "A. break 跳出本次循环，continue 跳出整个循环",
            "B. break 结束整个循环，continue 跳过本次剩下的、直接进下一轮",
            "C. 两者完全一样，只是写法不同",
            "D. break 只能用在 for，continue 只能用在 while",
        ],
        "answer": "B",
        "why": "break = 整个循环到此为止；continue = 这一轮不要了，下一轮继续。\n"
               "        猜数字里：猜错了用 continue（跳过本轮判断、不扣次数），"
               "猜对了或次数用完用 break。",
    },
    {
        "topic": "Day4 · 为什么 Agent 要捕获异常",
        "code": None,
        "q": "为什么 Agent 调用工具时一定要 try/except？",
        "options": [
            "A. 让代码运行得更快",
            "B. 工具失败时把错误变成字符串喂回模型，模型可以重试或换工具，而不是整个 Agent 崩掉",
            "C. 可以自动修复代码里的 bug",
            "D. Python 语法要求必须写",
        ],
        "answer": "B",
        "why": "一句话：异常是给程序看的，错误信息才是给模型看的。\n"
               "        不捕获 → 一个工具报错，整个 Agent 挂掉；"
               "捕获 → 把错误内容作为工具结果返回，模型自己决定下一步。",
    },
    {
        "topic": "Day6 · json.dumps 参数",
        "code": None,
        "q": 'json.dumps(data, ensure_ascii=False) 里 ensure_ascii=False 的作用是什么？',
        "options": [
            "A. 让文件体积更小",
            "B. 中文保持原样，不变成 \\u4f60\\u597d 这种转义",
            "C. 加快写入速度",
            "D. 自动加上缩进",
        ],
        "answer": "B",
        "why": "默认 ensure_ascii=True 会把所有非 ASCII 字符转成 \\uXXXX 转义。"
               "文件仍是合法 JSON，但人看不懂，调试时等于瞎一半。\n"
               "        indent=2 是另一件独立的事，负责换行缩进。",
    },
    {
        "topic": "Day6 · 路径为什么跟脚本走",
        "code": None,
        "q": 'DATA_FILE = Path(__file__).parent / "todo.json" 这样写解决了什么问题？',
        "options": [
            "A. 让数据文件的路径跟着脚本走，不管你在哪个目录下敲命令",
            "B. 自动创建不存在的文件",
            "C. 让文件读取得更快",
            "D. 让文件变成只读",
        ],
        "answer": "A",
        "why": "__file__ 是「这个脚本自己的路径」，.parent 取它所在的文件夹。\n"
               "        写成 Path(\"todo.json\") 则跟着「你此刻所在的目录」算，换个目录就指向别处"
               "—— Day4 那次打开空白文件就是它干的。",
    },
    {
        "topic": "Day6 · 编码",
        "code": None,
        "q": '读写含中文的文件时，encoding="utf-8" 为什么必须写？',
        "options": [
            "A. 不写会变慢",
            "B. Windows 中文系统默认按 GBK 打开，含中文会乱码或抛 UnicodeDecodeError",
            "C. 不写文件体积会变大",
            "D. 不写就是语法错误",
        ],
        "answer": "B",
        "why": "写和读必须用同一个编码。写的时候按 GBK、读的时候按 UTF-8，字节对不上就抛 "
               "UnicodeDecodeError —— 你上周亲眼见过 bb b5 b5 f4 c1 cb 那串字节。\n"
               "        另外记一句：UnicodeDecodeError 属于 ValueError，不属于 OSError。",
    },
    {
        "topic": "Day5 · 改动落在哪个函数",
        "code": None,
        "q": "计算器拆成 read_number / calculate / print_results / main 后，"
             "想加一条 // 整除结果，只改哪个函数？",
        "options": [
            "A. read_number",
            "B. calculate",
            "C. print_results",
            "D. main",
        ],
        "answer": "B",
        "why": "判断依据是「这件事属于哪一类动作」：读入 / 计算 / 显示 / 串联。"
               "多算一种运算是「计算」，所以改 calculate，往返回的字典里加一行。\n"
               "        print_results 一个字不用动，因为它遍历字典、有几对打几行。",
    },
    {
        "topic": "Day5 · 可变对象传参",
        "code": """
def add_item(box, item):
    box.append(item)
    return len(box)

nums = [1, 2, 3]
print(add_item(nums, 4))
print(nums)
""",
        "q": "输出是什么？",
        "options": [
            "A. 第一行 4，第二行 [1, 2, 3]",
            "B. 第一行 4，第二行 [1, 2, 3, 4]",
            "C. 第一行 3，第二行 [1, 2, 3, 4]",
            "D. 报错",
        ],
        "answer": "B",
        "why": "列表是可变对象，传进函数的是「同一个列表」，不是复制品。"
               "函数里 append 改的就是外面那个 nums。\n"
               "        想让调用方不受影响，得传 nums.copy()。这和数字、字符串不一样"
               "——那些改不了，看起来像复制。",
    },
    {
        "topic": "Day3 · 集合与字典的区别",
        "code": None,
        "q": '写 {"agent", 5} 和 {"agent": 5} 有什么区别？',
        "options": [
            "A. 完全一样，都是字典",
            "B. 前者是集合（无序、不重复），后者才是字典（键值对）",
            "C. 前者直接报错",
            "D. 前者是元组",
        ],
        "answer": "B",
        "why": "花括号里写 键: 值 才是字典；只写几个元素、用逗号隔开，是集合。"
               "集合用来去重和判断「在不在里面」，没有键的概念。\n"
               "        推导式里最容易踩：{x for x in ...} 得集合，{k: v for ...} 才是字典。",
    },
]


def ask_one(idx, item, total):
    """出一道题，返回 (用户答案, 是否答对)；用户按 q 时返回 (None, False)。"""
    print()
    print(LINE)
    print(f"第 {idx} 题 / 共 {total} 题")
    print(LINE)

    if item.get("code"):
        print("代码：")
        for one_line in item["code"].strip("\n").split("\n"):
            print("    " + one_line)
        print()

    print(item["q"])
    print()
    for opt in item["options"]:
        print("  " + opt)
    print()

    while True:
        ans = input("你的答案（A/B/C/D，q 退出）：").strip().upper()
        if ans == "Q":
            return None, False
        if ans in ("A", "B", "C", "D"):
            break
        print("  只输入 A、B、C、D 其中一个，或者 q 退出。")

    ok = ans == item["answer"]
    print()
    if ok:
        print("  [对]")
    else:
        print(f"  [错] 正确答案是 {item['answer']}")
    print(f"  解析：{item['why']}")
    return ans, ok


def main():
    total = len(QUESTIONS)
    print(LINE)
    print(f"Day7 巩固测验：Day2 ~ Day6，共 {total} 题")
    print("答完一题立刻给解析。输入 q 可以随时退出。")
    print(LINE)

    wrong = []
    done = 0

    for i, item in enumerate(QUESTIONS, 1):
        ans, ok = ask_one(i, item, total)
        if ans is None:
            print()
            print("已退出，本次不计成绩。想重来就再跑一遍这条命令。")
            return
        done += 1
        if not ok:
            wrong.append((i, item, ans))

    score = done - len(wrong)
    print()
    print(LINE)
    print(f"成绩：{score} / {done}   （{round(score / done * 100)} 分）")
    print(LINE)

    if not wrong:
        print("全对。Day2~Day6 的地基是实的，可以放心进 Day8 面向对象。")
        return

    print("错题回顾：")
    for i, item, ans in wrong:
        print(f"  第 {i} 题   你选 {ans}，正确 {item['answer']}   [{item['topic']}]")
    print()

    if score >= 10:
        print("10 题以上正确，可以继续往下走。错的那两题睡前再看一眼解析就行。")
    elif score >= 7:
        print("及格线上。把错题的解析再读一遍，然后翻出对应笔记重看那一节，不用重学整章。")
    else:
        print("低于 7 题，建议今天别急着进 Day8 ——")
        print("先回看 notes/day01_05_overview.md 里对应的章节，明天再测一次。")


if __name__ == "__main__":
    main()
