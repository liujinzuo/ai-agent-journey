# Day3 · 数据结构：列表 / 字典 / 元组 / 集合

- 日期：2026-11-04
- 教材：[Python 官方中文教程 · 数据结构](https://docs.python.org/zh-cn/3/tutorial/datastructures.html)
- 产出：`code/day03_wordcount.py`（统计英文文本词频 Top 20）
- 输入样例：`code/sample.txt`

---

## 一、一句话分工（先记这张表，语法随用随查）

| 结构      | 写法              | 一句话        | Agent 开发里对应什么        |
| ------- | --------------- | ---------- | -------------------- |
| `list`  | `["a", "b"]`    | 有序、能改、可重复  | 对话历史 `messages`、工具清单 |
| `dict`  | `{"name": "x"}` | 键值对，按键取值最快 | 工具参数、JSON、Agent 状态   |
| `tuple` | `("a", 1)`      | 有序、不能改     | 函数一次返回多个值            |
| `set`   | `{"a", "b"}`    | 自动去重、无序    | 去重、判断"在不在"           |

> 今天真正要会的是 **list 和 dict**，tuple / set 知道有这么个东西就行。

---

## 二、六个动作（会这六个就够用）

```python
msg = ["system", "user", "assistant"]

msg[0]              # "system"        索引，从 0 开始
msg[-1]             # "assistant"     负数 = 从后往前数
msg[0:2]            # ["system","user"]  切片，含头不含尾
msg.append("tool")  # 加到末尾
msg.remove("user")  # 按值删除，值不存在会报错
len(msg)            # 4  长度
"tool" in msg       # True  判断在不在
```

```python
tool = {"name": "search", "timeout": 10}

tool["name"]              # "search"  键不存在会报 KeyError
tool.get("timeout", 30)   # 10        取不到时给默认值，不报错 ← 更安全
tool["timeout"] = 20      # 改
tool["retries"] = 3       # 键不存在就是新增
del tool["retries"]       # 删
for k, v in tool.items(): # 同时拿键和值
    print(k, v)
```

**唯一必须记住的一行**（今天全篇最值

counts [W]=counts.get(w,0)+1

读法：取 `w` 的次数，没有就当 0，然后 +1 写回去。词频、投票、统计全用它。

---

## 三、列表推导式（把 3 行压成 1 行）

> 这一节是后补的（2026-11-08），配套练习：`code/day03_comprehension.py`
> 完整速查卡：`notes/python_comprehension_cheatsheet.md`（模板 + 13 种写法的实测输出 + 三个常见错）

```python
# 普通写法
nums = [1, 2, 3, 4, 5]
squares = []
for n in nums:
    squares.append(n * n)

# 推导式
squares = [n * n for n in nums]
```

带条件：

```python
even = [n for n in nums if n % 2 == 0]      # [2, 4]
```

字典推导式（把"单词→次数"反过来成"次数→单词"）：

```python
flip = {v: k for k, v in counts.items()}
```

推导式读起来是「对每个 n，产出 n*n」——**先说产出，再说来源**，习惯了会很顺。

**动手（10 分钟，这条尾巴就靠它补）**：

```
python code/day03_comprehension.py
```

脚本里有 6 个示例 + 3 个 TODO，把 TODO 改完再跑，自检会打 `[OK]`。  
改不出来就看提示行，三个都是「把 for 循环那几行搬进方括号」。

---

## 四、词频统计的四步（就是今天脚本的结构）

```
文件(str)
  ↓ 清洗：去标点、转小写、丢停用词
单词(list)
  ↓ 计数：counts[w] = counts.get(w, 0) + 1
词频(dict)
  ↓ 排序：sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
Top20(list[tuple])
```

关键点：

- `counts.items()` 把字典变成 `[(单词, 次数), ...]`
- `key=lambda kv: kv[1]` 表示按第 2 项（次数）排
- `[:20]` 切片取前 20

---

## 五、为什么 Agent 开发天天用这个

- 模型要求调用工具 → 返回的是 **dict**：`{"name": "search", "arguments": {...}}`
- 多轮对话 → 是 **list[dict]**：`[{"role":"user","content":"..."}, ...]`
- 任何 API 返回的 JSON → 解析出来就是 **dict + list**
- 检索到的文档、历史记忆 → 是 **list**

一句话：**Agent 编程 90% 的时间在跟 list 和 dict 打交道**，剩下的才是模型调用。

---

## 六、今日验收

- [ ] 跑通 `python code/day03_wordcount.py`，看到 Top 20
- [ ] 能说出 list 和 dict 的一句话区别（有序可改 vs 键值对）
- [ ] 能解释 `counts.get(w, 0)` 里那个 `0` 是干什么的
- [ ] 自己改一处并跑通（任选：加停用词 / 改 Top 10 / 换自己的文本文件）

## 附：为什么拿中文文本 / 源码当输入，会冒出一整串汉字？

跑 `python code/day03_wordcount.py code/day02_calculator.py` 时，榜单里会出现  
`请输入第一个数字`、`从键盘读两个数字` 这种整句中文——**这不是 bug**。

- `ch.isalpha()` 对汉字也返回 `True`，所以汉字被保留下来
- 但中文词与词之间**没有空格**，`.split()` 切不开，于是整句成了一个 token

这说明脚本确实在正常工作（把文本里所有字母和汉字都抓出来了）。

想只统计英文单词，在 `clean_words` 的过滤条件里加一个判断：

```python
return [w for w in raw if w not in STOPWORDS and len(w) >= 2 and w.isascii()]
```

中文正确分词要上专门的库（如 `jieba`），后面做 RAG 的「文本切分」时会正式遇到这个问题。

## 七、我踩的坑

> 挑一条真发生过的，写成自己的话：
>
> - 拿中文源码当输入，整句汉字变成一个「词」（`isalpha()` 对汉字也返回 True，但没空格切不开）
> - 推导式里 `if` 放前面和放后面含义不一样，搞混了
> - 排序那句 `key=lambda kv: kv[1]` 看不懂，先背下来了

- 拿中文源码当输入，整句汉字被当成一个「词」，因为 isalpha() 对汉字也返回 True，但中文没空格切不开。


## 八、一句话总结

> 参考：列表有序能改，字典按键取值；计数用 `counts.get(w, 0) + 1`，四行循环能压成一行推导式。

- 列表有序能改、字典按键取值；计数用 counts.get(w, 0) + 1，四行循环能压成一行推导式。

