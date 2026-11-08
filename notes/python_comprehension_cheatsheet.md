# Python 推导式速查卡

> 忘了就翻这里，不要背。本文所有输出都是实际跑过的。
> 一句话：**推导式 = 把 for 循环压进一对括号里。**

---

## 一、万能模板（四个位置，记住顺序）

```
[ 产出   for 变量 in 来源   if 条件 ]
   ↑            ↑              ↑
 要什么        从哪拿        只要满足的（可省略）
```

**念法**：对「来源」里的每个「变量」，如果满足「条件」，就产出「产出」。

例：`[n * n for n in nums if n % 2 == 0]`
读作：对 nums 里的每个 n，如果是偶数，就产出 n 的平方。

---

## 二、「我想…」→ 就这么写（全部实测）

| 我想要 | 写法 | 实测输出（nums=1~10, words=agent/tool/model/loop, counts={agent:5,tool:3,model:2}） |
|---|---|---|
| 每个都加工 | `[n * n for n in nums]` | `[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]` |
| 只挑一部分 | `[n for n in nums if n % 2 == 0]` | `[2, 4, 6, 8, 10]` |
| 每个都留但分两种处理 | `["偶" if n % 2 == 0 else "奇" for n in nums]` | `['奇','偶','奇','偶',…]` |
| 字符串转大写 | `[w.upper() for w in words]` | `['AGENT', 'TOOL', 'MODEL', 'LOOP']` |
| 按长度过滤再加工 | `[w.upper() for w in words if len(w) > 4]` | `['AGENT', 'MODEL']` |
| 字典：值全部翻倍 | `{k: v * 2 for k, v in counts.items()}` | `{'agent': 10, 'tool': 6, 'model': 4}` |
| 字典：只留值 > 2 | `{k: v for k, v in counts.items() if v > 2}` | `{'agent': 5, 'tool': 3}` |
| 字典：拼成 "键=值" | `[f"{k}={v}" for k, v in counts.items()]` | `['agent=5', 'tool=3', 'model=2']` |
| 集合：去重 | `{n % 3 for n in [1,2,3,4,5,6]}` | `{0, 1, 2}` |
| 带下标 | `{i: w for i, w in enumerate(words)}` | `{0:'agent', 1:'tool', 2:'model', 3:'loop'}` |
| 两层展开（扁平化） | `[x for row in [[1,2],[3,4]] for x in row]` | `[1, 2, 3, 4]` |
| 两两组合 | `[(a, b) for a in [1,2] for b in ["x","y"]]` | `[(1,'x'), (1,'y'), (2,'x'), (2,'y')]` |
| 求和（不用列表） | `sum(n * n for n in nums)` | `385` |

> 最后一条是「生成器表达式」：括号换成圆括号、或者当函数唯一参数时直接不写，
> 好处是不把整个列表造出来，省内存。大数据量时用它。

---

## 三、三种括号，对应三种容器

| 括号 | 得到 | 写法特点 |
|---|---|---|
| `[...]` | `list` | 产出随便写 |
| `{k: v ...}` | `dict` | 产出必须写成 `键: 值`，来源通常是 `xxx.items()` |
| `{x ...}` | `set` | 跟 list 一样，但会自动去重、无序 |

**判据**：要不要「键值对应」→ 要就用 `{}` + `键:值`；只关心「有哪些」→ `[...]`。

---

## 四、90% 的报错来自这三处

### 1. `if` 放前面还是后面，含义完全不同

```python
[n for n in nums if n % 2 == 0]           # 过滤：只要偶数，结果长度变短
["偶" if n % 2 == 0 else "奇" for n in nums]  # 二选一：每个都留，结果和原列表等长
```

记法：**`if` 在 `for` 后面 = 筛（可能变少）；`if...else` 整体在 `for` 前面 = 换（数量不变）。**

### 2. 产出里忘了写冒号（字典版）

```python
{k: v * 2 for k, v in counts.items()}   # 对
{v * 2 for k, v in counts.items()}      # 错：这变成 set 了，键丢了
```

### 3. 来源没写 `.items()`

```python
{k: v for k, v in counts.items()}   # 对
{k: v for k, v in counts}           # 错：ValueError，字典直接遍历只给键
```

---

## 五、写不出来就退回循环（这不是退步）

```python
# 想不清的时候，先写循环 —— 一定不会错
result = []
for item in source:
    if 条件:
        result.append(产出)

# 写通了再压成一行
result = [产出 for item in source if 条件]
```

**工程上的正解**：推导式只用来做**一层**的简单加工。
两层以上（嵌套 for 或嵌套 if...else）就写回循环 —— 三个月后你自己都看不懂。

---

## 六、Day3 练习的答案（对照用）

```python
evens_mine = [n for n in nums if n % 2 == 0]        # [2,4,6,8,10]
plural     = [w + "s" for w in words]               # ['agents','tools','models','loops']
doubled    = {k: v * 2 for k, v in counts.items()}  # {'agent':10,'tool':6,'model':4}
```

---

## 七、这东西在 Agent 开发里干什么

| 场景 | 写法 |
|---|---|
| 把历史消息里所有工具调用挑出来 | `[m for m in messages if m["role"] == "tool"]` |
| 把检索结果拼成一段上下文 | `"\n\n".join(d["text"] for d in docs)` |
| 工具名 → 函数对象，建工具表 | `TOOLS = {t.name: t.func for t in tool_list}` |
| 统计每个工具被调了几次 | `counts[name] = counts.get(name, 0) + 1` |
| 过滤掉空返回的工具结果 | `[r for r in results if r.get("ok")]` |

RAG 里那句 `[d for d in docs if d["score"] > 0.8]`，就是今天这个模板。

---

## 八、记忆锚点（只记这一行）

```
[产出 for 变量 in 来源 if 条件]
```

- 要字典：`{键: 值 for k, v in 字典.items()}`
- 写不出来：先写循环，再照三步搬
