# Day4 · 控制流与异常处理

- 日期：2026-11-05
- 教材：[Python 官方中文教程 · 更多控制流工具](https://docs.python.org/zh-cn/3/tutorial/controlflow.html)、[菜鸟教程 · 异常处理](https://www.runoob.com/python3/python3-exceptions.html)
- 产出：`code/day04_guess.py`（猜数字，带输入校验与异常提示）

---

## 一、分支：让程序做选择

```python
score = 85

if score >= 90:
    level = "A"
elif score >= 60:
    level = "B"
else:
    level = "C"
```

三个细节：

- `elif` 是"否则如果"，从上往下**只要有一个成立，后面的就不再判断**
- Python 靠**缩进**划分代码块，不是靠大括号。多一个空格都可能报错
- 条件表达式（一行写法）：`level = "A" if score >= 90 else "B"`

真值判断（写代码时经常靠这个偷懒）：

```python
if messages:            # 空列表 [] 视为假，非空为真
if not errors:          # 空列表 → not [] → True
if user_input.strip():  # 空字符串为假
```

---

## 二、循环：for 和 while 怎么选

| | 用在什么时候 | 例子 |
|---|---|---|
| `for` | 次数已知，或要遍历一个列表 | 遍历 `messages` 里的每条消息 |
| `while` | 次数未知，靠条件停 | Agent 主循环：一直跑到模型不再调用工具 |

```python
# for：遍历 + enumerate 同时拿序号
for i, msg in enumerate(messages, start=1):
    print(i, msg["role"])

# while：条件驱动
while step < max_steps:
    step += 1
```

**`break` 和 `continue` 的区别**（今天最容易混的一对）：

| 关键字 | 作用 | 一句话 |
|---|---|---|
| `break` | 直接跳出整个循环 | 不玩了，收摊 |
| `continue` | 跳过本次，进入下一次 | 这一次不算数，重来 |

猜数字里两个都用到了：用户输入 `q` → `return` 退出；输入 `abc` → `continue`，这次不扣次数。

```python
while used < MAX_TRIES:
    raw = input()
    try:
        guess = int(raw)
    except ValueError:
        continue        # 非法输入不扣次数，直接下一轮
    used += 1           # 只有合法输入才计数
```

---

## 三、异常：别让一行坏输入把程序弄死

`int("abc")` 会抛 `ValueError`。不接住，程序直接崩，前面所有的状态全丢。

```python
try:
    guess = int(raw)          # 可能出错的代码
except ValueError:
    print("这不是数字")        # 出错了怎么办
else:
    print(f"读到了 {guess}")   # 没出错才执行
finally:
    print("这一轮结束")        # 不管出不出错都执行
```

四件套的分工：

| 块 | 什么时候执行 | 用途 |
|---|---|---|
| `try` | 总是 | 把可能失败的代码放进去 |
| `except` | 出错时 | 兜底处理，别让程序崩 |
| `else` | 没出错时 | 正常路径，放"成功之后"的逻辑 |
| `finally` | 永远 | 清理资源：关文件、断连接、写日志 |

常见异常类型（认识就行，不用背）：

| 异常 | 什么情况 |
|---|---|
| `ValueError` | 类型对但值不对：`int("abc")` |
| `TypeError` | 类型不对：`"a" + 1` |
| `KeyError` | 字典里没这个键：`d["不存在"]` |
| `IndexError` | 列表下标越界：`[1,2][5]` |
| `ZeroDivisionError` | 除以 0 |
| `FileNotFoundError` | 文件不存在 |

---

## 四、为什么 Agent 必须捕获工具异常（今天最重要的一节）

Agent 干活的方式是：**模型说"我要调用某个工具" → 你的代码去执行 → 把结果还给模型 → 模型决定下一步**。

工具会以各种方式失败：网络超时、参数格式错、API 限流、权限不足、返回超大 JSON。

**不捕获的后果**：程序抛异常退出，整个 Agent 死掉，用户看到一堆红色报错。

**捕获之后**：把错误**变成一段文字**，当成工具结果喂回模型 —— 模型看到 `"error: timeout"` 会自己决定重试或换个工具。这就是 Agent 的自我修复能力。

```python
def call_tool(name: str, args: dict) -> dict:
    """所有工具调用都必须经过这一层包装。"""
    try:
        result = TOOLS[name](**args)
        return {"ok": True, "result": result}
    except KeyError:
        return {"ok": False, "error": f"没有名为 {name} 的工具"}
    except Exception as e:
        # 关键：不要把异常抛给用户，要把它变成模型能读的字符串
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}
```

三句话记住：

1. **异常是给程序看的，错误信息才是给模型看的**
2. Agent 的鲁棒性不来自模型多聪明，来自**每一个工具都有兜底**
3. `except Exception as e` 里一定要带上 `type(e).__name__`，否则你只会看到 "出错了"，不知道是哪种错

---

## 五、今日验收

- [ ] 跑通 `python code/day04_guess.py`，能正常猜一局
- [ ] 输入 `abc` 和 `200`，确认程序**不崩**、不扣次数
- [ ] 能说出 `break` 和 `continue` 的区别
- [ ] 能说出 `finally` 在什么时候执行
- [ ] 能用一句话解释"为什么 Agent 调工具要 try/except"

## 六、我踩的坑

-

## 七、一句话总结

-
