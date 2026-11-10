"""Day1~Day5 知识点速览：一条命令跑完全部小例子。

跑法：python code/recap_day1_5.py
对照：notes/day01_05_overview.md
"""


def section(title):
    print()
    print("=" * 48)
    print(title)
    print("=" * 48)


section("Day2-1  变量是「标签」，不是「盒子」")
name = "liujinzuo"
age = 30
print("name =", name, "| age =", age)
name = age
print("name = age 之后，name =", name, "（标签换去贴另一个值了）")

section("Day2-2  四种基本类型")
for v in [42, 3.14, "agent", True]:
    print(f"  {v!r:>10}  ->  {type(v).__name__}")

section("Day2-3  input() 拿到的永远是字符串（Day2 第一大坑）")
raw = "10"
print("  raw + '3'        =", raw + "3", "  <- 字符串拼接，不是加法")
print("  float(raw) + 3   =", float(raw) + 3, "  <- 转成数字才能算")

section("Day2-4  / 是小数除法，// 是整除")
print("  10 / 3  =", 10 / 3)
print("  10 // 3 =", 10 // 3)
print("  10 % 3  =", 10 % 3)
print("  2 ** 10 =", 2 ** 10)

section("Day2-5  f-string：把变量塞进句子")
a, b = 10.0, 3.0
print(f"  {a} + {b} = {a + b}")

section("Day3-1  列表：有序、能改、能切")
nums = [1, 2, 3, 4, 5]
nums.append(6)
print("  append 之后:", nums)
print("  第一个:", nums[0], "| 最后一个:", nums[-1])
print("  前三个  :", nums[:3])

section("Day3-2  字典：按键取值，键不用是数字")
tool = {"name": "search", "args": {"q": "agent"}}
print("  tool['name']          ->", tool["name"])
print("  tool.get('timeout', '没设置') ->", tool.get("timeout", "没设置"))

section("Day3-3  计数万能一行：counts.get(w, 0) + 1")
text = "agent tool agent model agent"
counts = {}
for w in text.split():
    counts[w] = counts.get(w, 0) + 1
print(" ", counts)

section("Day3-4  推导式：[产出 for 变量 in 来源 if 条件]")
nums = [1, 2, 3, 4, 5, 6]
print("  只要偶数:", [n for n in nums if n % 2 == 0])
print("  每项平方:", [n * n for n in nums])
print("  字典版  :", {k: v * 2 for k, v in counts.items()})

section("Day4-1  分支：if / elif / else")
for score in [3, 5, 9]:
    if score <= 3:
        level = "神"
    elif score <= 5:
        level = "稳"
    else:
        level = "勉强"
    print(f"  用了 {score} 次 -> {level}")

section("Day4-2  break 跳出整个循环，continue 只跳过本次")
kept = []
for n in range(1, 6):
    if n == 2:
        continue
    if n == 5:
        break
    kept.append(n)
print("  留下的:", kept, "（2 被 continue 跳过，5 触发 break 结束）")

section("Day4-3  异常：别让一行坏输入把程序搞崩")


def read_number(raw):
    try:
        return float(raw)
    except ValueError:
        return None


for raw in ["10", "abc", "3.5"]:
    print(f"  输入 {raw!r:>6} -> {read_number(raw)}")

section("Day5-1  函数：入口 -> 加工 -> 出口")


def add(a, b):
    """两数相加。"""
    return a + b


print("  add(3, 4) =", add(3, 4))

section("Day5-2  return 交给程序，print 只给人看")


def say_hello():
    print("  hello, Agent        <- 这是 print 打出来的")
    # 这里没有 return


x = say_hello()
print("  say_hello() 的返回值是:", x)

section("Day5-3  默认参数：调用时可以少传")


def greet(name, greeting="你好"):
    return f"{greeting}，{name}"


print(" ", greet("liujinzuo"))
print(" ", greet("liujinzuo", "早上好"))

section("Day5-4  一个函数只干一件事：算的不管显示")


def calculate(a, b):
    return {"+": a + b, "-": a - b, "*": a * b, "/": a / b, "//": a // b}


def print_results(a, b, results):
    for op, value in results.items():
        print(f"  {a} {op} {b} = {value}")


print_results(10.0, 3.0, calculate(10.0, 3.0))
print("  （新加的 // 自动出现，print_results 一个字都没改）")

section('Day5-5  if __name__ == "__main__" 是干什么的')
print("  直接运行本文件时，__name__ =", __name__)
print("  被别的文件 import 时，__name__ = 模块名，所以 main() 不会自动跑")

print()
print("全部例子跑完了。Day1 是环境与 Git，没有语法例子，命令见 notes/day01_05_overview.md")
