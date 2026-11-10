# Python 函数速查卡

> 忘了就翻这里，不用背。本文输出都是 `python code/day05_functions.py` 实跑出来的。
> 一句话：**函数 = 把一段代码打包，给它名字，可以反复调用。**

---

## 一、最小形态（背下这四行就够起步）

```python
def add(a, b):        # def 函数名(参数列表):
    """两数相加。"""   # docstring：写一句话说明干什么，Agent 靠它理解你的工具
    return a + b      # return：把结果交出去

print(add(3, 4))      # 7
```

四条硬规矩：

- `def` 开头，**冒号不能少**
- 函数体**必须缩进**（4 个空格）
- 要交结果出去就写 `return`，不写就返回 `None`
- 参数名和 docstring 是给人和 AI 看的，**写得清楚比写得短重要**

---

## 二、参数的五种形态（今天唯一需要看的表）

| 写法 | 名称 | 调用 | 打包成 | 什么时候用 |
|---|---|---|---|---|
| `def f(a, b)` | 位置参数 | `f(1, 2)` | — | 最常用 |
| `def f(a, b=2)` | 默认参数 | `f(1)` | — | 大部分调用用同一个值 |
| `def f(*args)` | 任意位置参数 | `f(1, 2, 3)` | `tuple` | 参数个数不定，如 `print` |
| `def f(**kwargs)` | 任意关键字参数 | `f(x=1, y=2)` | `dict` | 一堆可选的配置项 |
| `def f(a, *, b)` | 强制关键字 | `f(1, b=2)` | — | 防止调用方传错位置 |

实跑对照：

```python
greet("小明")              # 你好，小明
greet("小明", "早")        # 早，小明          ← 用了默认值又被覆盖

total(1, 2, 3, 4)          # 10                ← *args 收成 (1,2,3,4)

build_tool("search", timeout=10, retries=3)
# {'name': 'search', 'timeout': 10, 'retries': 3}   ← **kwargs 收成 dict
```

**默认参数必须放最后**：`def f(a=1, b)` 是语法错误。

---

## 三、`return` 和 `print` 的区别（最容易混的一对）

| | 作用 | 能不能拿去用 |
|---|---|---|
| `return` | 把结果**交回**调用者，函数立刻结束 | 能：`x = add(1, 2)` → `x` 是 `3` |
| `print` | 把东西**显示**到屏幕，函数继续往下跑 | 不能：`x = print(3)` → `x` 是 `None` |

实跑演示：

```python
say_hello()      # 屏幕上打出 hello, Agent
                 # 但它的返回值 = None
```

**一句话记**：`print` 是给人看的，`return` 是给程序用的。想拿结果继续算，必须 `return`。

---

## 四、三个必踩的坑

### 坑 1 · 可变默认值（面试级陷阱）

```python
def bad(item, box=[]):      # 错：这个 [] 只创建一次，所有调用共享
    box.append(item)
    return box

def good(item, box=None):   # 对：调用时再创建
    if box is None:
        box = []
    box.append(item)
    return box
```

`bad()` 调两次会得到 `['a', 'b']`——第一次的结果被记住了。**默认值永远不要写 `[]` / `{}`。**

### 坑 2 · 函数里改外部变量不生效

```python
counter = 0

def bump_bad():
    counter = counter + 1    # 这只是新建了一个局部变量，外面的 counter 没变

def bump_good():
    global counter           # 声明：我要改外面那个
    counter += 1
```

实跑结果：`bump_bad()` 之后全局还是 `0`，`bump_good()` 之后才变 `1`。

**工程上的正解**：别用 `global`，把值当参数传进去、用 `return` 拿出来。

### 坑 3 · 忘了 `return`

```python
def add(a, b):
    a + b          # 算完就丢了

x = add(1, 2)      # x 是 None
```

屏幕不报错，结果悄悄没了。这就是为什么“没报错”不等于“对”。

---

## 五、lambda：一次性的小函数

```python
square = lambda n: n * n          # 等价于 def square(n): return n * n
sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
```

只用来「临时传给别的函数」，**不要赋值给变量长期用**——那样应该写成 `def`。

---

## 六、什么时候该拆函数（三条判断标准）

1. 一段代码**能用一句话说清它干什么** → 可以拆
2. 这段代码**在别处还会用到** → 应该拆
3. 拆出来**需要传 5 个以上参数** → 拆错了，切分位置不对

再加一条：**算和显示必须分开**。`calculate()` 只算（`return` dict），`print_results()` 只打印，
这样算的部分以后能直接给网页、API、测试用。

---

## 七、为什么 Agent 开发离不开函数

**在 Agent 里，工具（tool）就是一个函数。** 模型看不到你的代码，它只看三样东西：

| 模型能看到的 | 对应代码 | 写不好的后果 |
|---|---|---|
| 函数名 | `get_weather` | 叫 `f1` 模型就不知道该不该用 |
| 参数名 + 类型 | `city: str` | 叫 `a` 模型会瞎猜 |
| docstring | `"""查询某城市天气"""` | 没写，模型不知道何时调用 |

所以 Day5 不是“学语法”，是在**造零件**。Day40 写 Function Calling 时，你今天写的每个函数都会被直接包成工具。

---

## 八、记忆锚点

```python
def 名字(参数):
    """干什么"""
    return 结果
```

- 要交结果：`return`；只是显示：`print`
- 默认值别写 `[]` / `{}`
- 拆函数：一句话能说清 + 会用第二次 + 参数不超过 4 个
