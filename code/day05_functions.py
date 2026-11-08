"""
Day5 · 函数与模块化：把一段逻辑装进盒子，起个名字

    python code/day05_functions.py

七种写法，跑一遍就知道每种的形状。看完再去看 notes/Day05.md 的速查表。
"""

# ---------- 1. 最基础的函数：有输入、有输出 ----------


def add(a, b):
    """返回 a + b。注意 return 和 print 的区别，文末有演示。"""
    return a + b


# ---------- 2. 默认参数 ----------


def greet(name, prefix="你好"):
    """不传 prefix 时用默认值。默认参数必须放在参数列表最后。"""
    return f"{prefix}，{name}"


# ---------- 3. 没有 return 的函数，返回 None ----------


def say_hello(name):
    """只有副作用（打印），没有返回值。"""
    print(f"  hello, {name}")


# ---------- 4. *args：接受任意多个位置参数 ----------


def total(*numbers):
    """*numbers 把传进来的所有参数打包成一个 tuple。"""
    return sum(numbers)


# ---------- 5. **kwargs：接受任意多个关键字参数 ----------


def build_tool(name, **options):
    """**options 打包成一个 dict —— 这就是工具参数长什么样。"""
    return {"name": name, **options}


# ---------- 6. lambda：一次性的小函数 ----------

pairs = [("agent", 5), ("tool", 3), ("task", 4)]
by_count = sorted(pairs, key=lambda kv: kv[1], reverse=True)

# ---------- 7. 作用域 ----------

counter = 0          # 全局变量


def bump_bad():
    counter = 1      # 这里其实新建了一个局部变量，全局那个没动


def bump_good():
    global counter   # 明确声明：我要改的是外面那个
    counter += 1


def main():
    print("1) add(3, 4) =", add(3, 4))

    print("2) greet('小明')      =", greet("小明"))
    print("   greet('小明', '早') =", greet("小明", "早"))

    print("3) say_hello 没有 return，它返回的是：")
    result = say_hello("Agent")
    print("   返回值 =", result)

    print("4) total(1, 2, 3, 4) =", total(1, 2, 3, 4))

    print("5) build_tool('search', timeout=10, retries=3) =")
    print("   ", build_tool("search", timeout=10, retries=3))

    print("6) 按次数排序：", by_count)

    print("7) 全局 counter 初始 =", counter)
    bump_bad()
    print("   bump_bad()  之后 =", counter, "（没变：它改的是局部变量）")
    bump_good()
    print("   bump_good() 之后 =", counter, "（变了：它声明了 global）")

    print()
    print("记住：return 把结果交出去，print 只是给人看。")


if __name__ == "__main__":
    main()
