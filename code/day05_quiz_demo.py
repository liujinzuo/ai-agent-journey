"""Day5 小实验：给 calculate 加一条 // 整除，看 print_results 要不要跟着改。

跑法：python code/day05_quiz_demo.py
预期：打印 5 行，最后一行是 10.0 // 3.0 = 3.0
"""


def calculate(a, b):
    """和 day02_calculator_func.py 里的 calculate 一模一样，只多了一行 "//"。"""
    return {
        "+": a + b,
        "-": a - b,
        "*": a * b,
        "/": a / b,
        "//": a // b,      # <- 本次唯一的新增
    }


def print_results(a, b, results):
    """完全没改：它只负责遍历字典，不关心里面有哪些运算符。"""
    for op, value in results.items():
        print(f"{a} {op} {b} = {value}")


print_results(10.0, 3.0, calculate(10.0, 3.0))

print()
print("上面第 5 行是新增的整除结果，而 print_results 一个字都没改。")
