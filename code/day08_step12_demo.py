"""Day8 第一、二步的最小例子：手写 class  vs  @dataclass

运行：
    python code/day08_step12_demo.py

这个文件只做一件事：把同一段数据用两种写法各写一遍，
然后逐条打印结果，让你亲眼看到差别在哪。
"""

import inspect
from dataclasses import dataclass


def section(title):
    print()
    print("=" * 62)
    print(title)
    print("=" * 62)


# ================================================================
# 第一步：手写 class —— 自己写 __init__，把参数一个个搬到 self 上
# ================================================================

class Dog:
    """一条狗。名字和年龄是它的两个字段。"""

    def __init__(self, name, age):
        self.name = name          # 把外面的 name 存到"这条狗自己"身上
        self.age = age            # 把外面的 age 存到"这条狗自己"身上

    def bark(self):
        return f"{self.name} 汪汪叫"


# ================================================================
# 第二步：@dataclass —— 同一件事，只写"有哪些字段"，不写搬运
# ================================================================

@dataclass
class DogAuto:
    name: str                     # 只声明"有个名字，是字符串"
    age: int                      # 只声明"有个年龄，是整数"

    def bark(self):
        return f"{self.name} 汪汪叫"


# 再多一组：6 个字段时，差距会很明显
class ResultByHand:
    def __init__(self, tool, ok, data, error, cost, trace):
        self.tool = tool
        self.ok = ok
        self.data = data
        self.error = error
        self.cost = cost
        self.trace = trace


@dataclass
class ResultAuto:
    tool: str
    ok: bool
    data: str
    error: str
    cost: float
    trace: str


def main():
    print("Day8 · 第一步和第二步的最小例子")

    # ------------------------------------------------------------
    section("第一步 · 造一条狗，然后问它几个问题")
    # ------------------------------------------------------------
    d1 = Dog("旺财", 3)
    print('代码：d1 = Dog("旺财", 3)')
    print()
    print(f"  d1.name    -> {d1.name}")
    print(f"  d1.age     -> {d1.age}")
    print(f"  d1.bark()  -> {d1.bark()}")
    print()
    print("  说明：")
    print("    Dog(...) 那一刻，__init__ 自动跑，把 '旺财' 存成 self.name")
    print("    之后 d1.name 就能取出来。你没有手动调 __init__，是 Python 调的。")
    print("    bark() 里的 self.name 指的就是'这条狗自己的名字'。")

    # ------------------------------------------------------------
    section("第一步 · 再说明：每条狗是独立的，改一条不影响另一条")
    # ------------------------------------------------------------
    d1 = Dog("旺财", 3)
    d2 = Dog("来福", 5)
    print('代码：d1 = Dog("旺财", 3)   d2 = Dog("来福", 5)')
    print()
    print(f"  d1 -> {d1.name}，{d1.age} 岁")
    print(f"  d2 -> {d2.name}，{d2.age} 岁")
    print()
    print("  现在只改 d1.age = 4：")
    d1.age = 4
    print(f"  d1 -> {d1.name}，{d1.age} 岁")
    print(f"  d2 -> {d2.name}，{d2.age} 岁    <- 没变")
    print()
    print("  说明：class 是模具，每条狗是单独压出来的，各存各的数据。")

    # ------------------------------------------------------------
    section("第二步 · 同一个东西用 @dataclass 写，用法完全一样")
    # ------------------------------------------------------------
    a1 = DogAuto("旺财", 3)
    print('代码：a1 = DogAuto("旺财", 3)')
    print()
    print(f"  a1.name    -> {a1.name}")
    print(f"  a1.age     -> {a1.age}")
    print(f"  a1.bark()  -> {a1.bark()}")
    print()
    print("  说明：构造函数、取值、方法，用法和手写版一模一样。")
    print("  区别只在于：__init__ 那两行 self.x = x，你不用写了。")

    # ------------------------------------------------------------
    section("第二步 · dataclass 白送的三样东西（逐条对比）")
    # ------------------------------------------------------------

    print("① __init__：造对象时收参数、存字段")
    print()
    hand_lines = len(inspect.getsource(ResultByHand).splitlines())
    auto_lines = len(inspect.getsource(ResultAuto).splitlines())
    print(f"   手写版     {hand_lines} 行，其中 6 行是 self.x = x 这样的赋值")
    print(f"   dataclass  {auto_lines} 行，赋值 0 行，只声明字段名和类型")
    print()
    print("   注意：总行数其实差不多！所以省的不是行数，是别的东西：")
    print("   手写版你漏写一行 self.error = error，程序照样创建成功，")
    print("   直到你取 obj.error 才炸 AttributeError —— 又是'错在A、报在B'。")
    print("   dataclass 字段表就是唯一依据，少声明一个、多传一个，当场 TypeError。")
    print()

    print("② __repr__：打印对象时显示什么")
    print(f"   手写版    -> {Dog('旺财', 3)}")
    print(f"   dataclass -> {DogAuto('旺财', 3)}")
    print("   手写版那串 0x... 是内存地址，你根本看不出里面装了什么。")
    print()

    print("③ __eq__：两个对象怎么算相等")
    print(f"   手写版     Dog('旺财',3) == Dog('旺财',3)   -> {Dog('旺财', 3) == Dog('旺财', 3)}")
    print(f"   dataclass  DogAuto('旺财',3) == DogAuto('旺财',3) -> {DogAuto('旺财', 3) == DogAuto('旺财', 3)}")
    print("   手写版比的是'是不是同一个对象'，所以 False；")
    print("   dataclass 比的是'每个字段的值是否都相同'，所以 True。")

    # ------------------------------------------------------------
    section("为什么这件事在 Agent 里重要")
    # ------------------------------------------------------------
    print("假设你用 dict 记一条对话：")
    msg = {"role": "user", "content": "你好"}
    print(f"  {msg}")
    print()
    print("现在把它打错一个字母：")
    bad = {"rloe": "user", "content": "你好"}
    print(f"  {bad}")
    print("  这个 dict 创建成功了，没有任何报错。")
    print("  直到你去取 bad['role']，才会炸 KeyError。")
    print("  → 错在写的地方，报在取的地方，中间可能隔了几百行。")
    print()
    print("换成 dataclass：")
    print('  Message(rloe="user", content="你好")')
    print("  → 造对象那一刻就报 TypeError: unexpected keyword argument 'rloe'")
    print("  → 错在哪一行，报就在哪一行。")
    print()
    print("这就是今天全部的意义：")
    print("  不是 dataclass 更短、更好看，")
    print("  而是它让你在写错的那一刻就知道，而不是半夜调 bug 时才知道。")

    print()
    print("=" * 62)
    print("跑完了。下一步：python code/day08_dataclass.py （六节完整演示）")
    print("=" * 62)


if __name__ == "__main__":
    main()
