# Day5 · 函数与模块化

- 日期：2026-11-06
- 教材：[Python 官方中文教程 · 定义函数](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions)
- 产出：把 `code/day02_calculator.py` 重构成 **多个函数 + main() 入口**

---

> 速查卡（今天只需要看这张）：`notes/python_function_cheatsheet.md`
> 实跑演示：`python code/day05_functions.py`（七种写法） / `python code/day05_verify.py`（重构验收）

## 一、什么时候该写函数

一句判断标准：**这段代码你能用一句话给它起个名字，就该抽成函数。**

三个信号：

1. 同样的代码出现两次以上
2. 一段逻辑能独立完成一件事
3. 你想给它加一行注释说"这里是在干 XX"

函数不是"高级写法"，是**给逻辑命名**。名字起对了，代码自己会讲话。

---

## 二、最小形态

```python
def add(a, b):
    return a + b

result = add(3, 4)      # 7
```

三件事：

- `def` 是定义，调用时写名字加括号
- 括号里是**输入**（参数），`return` 后面是**输出**
- 没有 `return` 的函数，返回值是 `None`

---

## 三、参数的五种形态

| 写法 | 名称 | 调用示例 | 打包成什么 |
|---|---|---|---|
| `def f(a, b)` | 位置参数 | `f(1, 2)` | — |
| `def f(a, b=2)` | 默认参数（**必须放最后**） | `f(1)` | — |
| `def f(*args)` | 任意位置参数 | `f(1, 2, 3)` | `tuple` |
| `def f(**kwargs)` | 任意关键字参数 | `f(x=1, y=2)` | `dict` |
| `def f(a, *, b)` | 强制关键字 | `f(1, b=2)` | — |

今天重点看 `*args` 和 `**kwargs` —— 它们打包成的 `tuple` / `dict`，正是 Day3 学的那两种结构。

```python
def total(*numbers):        # numbers 是 tuple
    return sum(numbers)

def build_tool(name, **options):     # options 是 dict
    return {"name": name, **options}

build_tool("search", timeout=10)     # {'name': 'search', 'timeout': 10}
```

---

## 四、`return` 和 `print` 的区别（今天最容易混的一对）

| | 作用 | 能不能拿去用 |
|---|---|---|
| `return` | 把结果**交回**调用者，函数立刻结束 | 能：`x = add(1, 2)` → `x` 是 `3` |
| `print` | 把东西**显示**出来，函数继续往下走 | 不能：`x = print(3)` → `x` 是 `None` |

```python
x = add(3, 4)       # x = 7        ✅ 拿到了结果
y = print(3 + 4)    # 屏幕显示 7，但 y = None  ❌
```

**经验**：函数内部尽量 `return`，把 `print` 留给最外层的 `main()`。这样函数才能被复用、被测试。

---

## 五、lambda：一次性的小函数

```python
pairs = [("agent", 5), ("tool", 3), ("task", 4)]
by_count = sorted(pairs, key=lambda kv: kv[1], reverse=True)
# [('agent', 5), ('task', 4), ('tool', 3)]
```

只在"作为参数传进去、用完就扔"时用它。**别写 `f = lambda x: x + 1`** —— 那种情况请老老实实用 `def`，因为函数该有名字。

---

## 六、作用域

- 函数内部**能读**外面的变量
- 想在函数里**改**外面的变量，要写 `global`（但尽量别这么干）
- 更好的做法：**用参数传进去，用 return 带出来**

```python
counter = 0

def bump_bad():
    counter = 1     # 新建了一个局部变量，全局那个没动

def bump_good():
    global counter  # 明确声明要改外面那个
    counter += 1
```

---

## 七、重构 `day02_calculator.py`：五步法

**第 1 步 · 圈出独立逻辑段**

原来的代码就三段：读两个数 → 算四个结果 → 打印四个结果。

**第 2 步 · 每段起个名字**

| 这一段 | 函数名 |
|---|---|
| 读两个数字 | `read_number()` / `read_two_numbers()` |
| 算四个结果 | `calculate()` |
| 打印结果 | `print_results()` |

**第 3 步 · 定输入和输出**

| 函数 | 输入（参数） | 输出（return） |
|---|---|---|
| `read_number(prompt)` | 提示语 | 一个 float |
| `calculate(a, b)` | 两个数 | 一个 dict（运算符 → 结果） |
| `print_results(a, b, results)` | 数字和结果 | 无（只打印） |

**第 4 步 · 用 `main()` 串起来**

**第 5 步 · 底部加固定写法**

```python
if __name__ == "__main__":
    main()
```

这行的意思是：**只有直接运行这个文件时才执行 main()，被别的文件 import 时不执行。**

---

## 八、为什么这是 Agent 开发的必修课

**在 Agent 里，工具（tool）就是一个函数。**

模型不会读你的代码，它只看三样东西：

1. **函数名** —— 让人（和模型）一眼知道这是干什么的
2. **参数名和类型** —— 知道要传什么进去
3. **docstring** —— 用人话说明什么时候该用它

```python
def get_weather(city: str, unit: str = "celsius") -> str:
    """查询指定城市的当前天气。city 传中文城市名，如"北京"；unit 可选 celsius / fahrenheit。"""
    ...
```

Day5 之后你写的每一个规范函数，都是在为 Day40 之后的 Function Calling 打地基 —— **你函数写得多清楚，你的 Agent 就有多可靠**。

---

## 九、今日验收

- [ ] 跑通 `python code/day05_functions.py`，七种写法都能对上号
- [ ] 能说出 `return` 和 `print` 的区别
- [ ] 把 `day02_calculator.py` 重构成 **至少 3 个函数 + main()**
- [ ] 重构后输入 `10` 和 `3`，输出和原来**一字不差** ← 这是重构的唯一验收标准
- [ ] 能说出 `*args` 和 `**kwargs` 各自打包成什么类型

---

## 十、参考答案（自己写完再看）

```python
"""Day2 重构版：命令行计算器（函数 + main 入口）。"""


def read_number(prompt: str) -> float:
    """读一个数字。加分项：输错了重问（用 Day4 的 try/except）。"""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("  这不是数字，重来")


def calculate(a: float, b: float) -> dict[str, float]:
    """返回四个运算结果，键是运算符。"""
    return {"+": a + b, "-": a - b, "*": a * b, "/": a / b}


def print_results(a: float, b: float, results: dict[str, float]) -> None:
    """把结果打成四行。没有 return，只负责显示。"""
    for op, value in results.items():
        print(f"{a} {op} {b} = {value}")


def main() -> None:
    a = read_number("请输入第一个数字: ")
    b = read_number("请输入第二个数字: ")
    print_results(a, b, calculate(a, b))


if __name__ == "__main__":
    main()
```

> 只想做"纯重构"（不加输入校验）的话，`read_number` 里就两行：
> `raw = input(prompt).strip()` 然后 `return float(raw)`。

---

## 十一、我踩的坑

-

## 十二、一句话总结

-
