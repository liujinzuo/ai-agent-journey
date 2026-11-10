"""Day5：命令行计算器（重构版）。

和 code/day02_calculator.py 功能完全一样，只是把 4 段逻辑拆成了 4 个函数：
    read_number()   —— 读一个数字
    calculate()     —— 算四则运算，返回 dict
    print_results() —— 按固定格式打印
    main()          —— 串起来

验收标准：输入 10 和 3，输出必须和原版一字不差。

拆函数的三条判断标准：
    1. 一段代码能用一句话说清它在干什么 → 可以拆
    2. 这段代码在别处还会用到 → 应该拆
    3. 拆出来需要传 5 个参数 → 拆错了，说明切分位置不对

运行：python code/day02_calculator_func.py
"""


def read_number(prompt: str) -> float:
    """读一个数字并转成 float。

    input() 拿到的永远是字符串，所以这里必须 float()。
    把「提示语」做成参数，两个数字就能复用一个函数。
    """
    raw = input(prompt)
    return float(raw)


def calculate(a: float, b: float) -> dict:
    """四则运算，返回一个 dict：{运算符: 结果}。

    返回 dict 而不是四个变量，好处是调用方一个变量就能拿到全部结果，
    而且后面要加 // % ** 时，只改这一个函数。
    """
    return {
        "+": a + b,
        "-": a - b,
        "*": a * b,
        "/": a / b,
    }


def print_results(a: float, b: float, results: dict) -> None:
    """把结果打印成 "10.0 + 3.0 = 13.0" 这种格式。

    没有 return，返回 None —— 这类函数叫「副作用函数」：它的作用就是打印。
    """
    for op, value in results.items():
        print(f"{a} {op} {b} = {value}")


def main() -> None:
    """入口：只做调度，不写业务细节。"""
    a = read_number("请输入第一个数字: ")
    b = read_number("请输入第二个数字: ")
    results = calculate(a, b)
    print_results(a, b, results)


# 固定写法：只有直接运行这个文件时才执行 main()
# 被别人 import 时不会自动跑（Day6 之后会用到这个特性）
if __name__ == "__main__":
    main()
