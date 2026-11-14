"""Day8 补充：漏写一个字段，两种写法各会发生什么

运行：
    python code/day08_missing_field_demo.py

场景：一次工具调用的结果，本来有 4 个字段
    tool   工具名
    ok     成功与否
    data   返回的数据
    error  失败原因（成功时是空字符串）

现在模拟"漏掉第 4 个字段"这个人为失误。
"""

from dataclasses import dataclass


def section(title):
    print()
    print("=" * 62)
    print(title)
    print("=" * 62)


# ================================================================
# 手写版：__init__ 是我自己写的函数
# 我在里面漏写了一句 self.error = error
# ================================================================

class ResultByHand:
    def __init__(self, tool, ok, data, error):
        self.tool = tool
        self.ok = ok
        self.data = data
        # ← 这里漏写了 self.error = error
        #   注意：上面这行是"注释"，不是删掉参数，参数 error 还在，
        #   只是没有人把它存到对象身上。


# ================================================================
# dataclass 版：我只声明字段
# 我漏声明了 error 这个字段
# ================================================================

@dataclass
class ResultAuto:
    tool: str
    ok: bool
    data: str
    # ← 这里漏声明了 error: str


def main():
    print("Day8 补充 · 漏写一个字段会怎样")

    # ------------------------------------------------------------
    section("一、手写版：创建对象，看它报不报错")
    # ------------------------------------------------------------
    print('代码：r = ResultByHand(tool="search", ok=True, data="3 条结果", error="")')
    print()
    r = ResultByHand(tool="search", ok=True, data="3 条结果", error="")
    print(f"  结果：{r}")
    print()
    print("  → 没有任何报错。对象造出来了。")
    print("  → 因为 __init__ 这个函数正常返回了，Python 认为一切正常。")

    # ------------------------------------------------------------
    section("二、手写版：现在去用那第 4 个字段")
    # ------------------------------------------------------------
    print("代码：print(r.error)")
    print()
    try:
        print(r.error)
    except AttributeError as e:
        print(f"  AttributeError: {e}")
    print()
    print("  → 报错了。但请注意：报错的位置在这里，")
    print("    而真正的失误（漏写 self.error = error）在你几十行之前写的 __init__ 里。")
    print()
    print("  这就是'错在A、报在B'：")
    print("    失误点：__init__ 里少写一行 —— 当时一声不响")
    print("    爆发点：别人读 r.error —— 这里才炸")

    # ------------------------------------------------------------
    section("三、dataclass 版：同样的失误，还没创建对象就炸了")
    # ------------------------------------------------------------
    print('代码：ResultAuto(tool="search", ok=True, data="3 条结果", error="")')
    print()
    try:
        ResultAuto(tool="search", ok=True, data="3 条结果", error="")
    except TypeError as e:
        print(f"  TypeError: {e}")
    print()
    print("  → 对象一个都没造出来，当场就被拦住了。")
    print("  → 因为 dataclass 的字段表就是参数表，两者不可能不一致：")
    print("     你声明了 3 个字段 → 构造函数只收 3 个参数")
    print("     你传了 4 个参数   → 多出来的 error 无处可去 → 立刻报错")

    # ------------------------------------------------------------
    section("四、把两个报错放在一起对比")
    # ------------------------------------------------------------
    print("  手写版（漏写赋值）：")
    print("     创建时：成功，无提示")
    print("     使用时：AttributeError —— 在几十行之后才炸")
    print("     你要做的事：往回翻，找出哪个字段没赋值（可能要找十分钟）")
    print()
    print("  dataclass（漏声明字段）：")
    print("     创建时：TypeError —— 就炸在这一行")
    print("     使用时：根本走不到这一步")
    print("     你要做的事：看报错里的字段名，补一行声明（十秒）")

    # ------------------------------------------------------------
    section("五、一句话")
    # ------------------------------------------------------------
    print("  手写版：参数表和赋值语句是两份东西，你写了参数、忘了赋值，")
    print("          Python 不会替你检查，它们不一致也没人拦。")
    print()
    print("  dataclass：字段表就是唯一依据，参数表由它生成，")
    print("          两者天生一致，所以任何不一致都会在门口被拦下。")
    print()
    print("  这就是'省的是错误空间，不是打字量'的意思：")
    print("  行数差不了几行，但你犯错的机会少了一大类。")

    print()
    print("=" * 62)
    print("跑完了。")
    print("=" * 62)


if __name__ == "__main__":
    main()
