# Day8 · 面向对象与 dataclass

> 配套脚本：`code/day08_dataclass.py`（跑一遍，六节演示全在里面）
> 今天的产出：`Message(role, content)` 和 `ToolCall(name, arguments)` 两个数据类

---

## 零、今天为什么学这个

你现在会用 dict 装数据，看起来够用了：

```python
msg = {"role": "user", "content": "你好"}
```

但 Agent 里一天要处理成千上万条这样的消息，dict 有三个躲不掉的毛病。今天的全部内容，就是为了解决这三个毛病。

---

## 一、dict 的三个毛病

| 毛病 | 具体表现 | 后果 |
|---|---|---|
| **拼错字没人管** | `{"rloe": "user"}` 照样创建成功 | 错在写的地方，报在几百行之外 |
| **没有类型** | `msg["content"]` 可能是字符串，也可能是 None | 要等到用它的时候才发现不对 |
| **不知道有哪些字段** | 拿到一个 dict，不知道它该有什么 | 每次都得翻文档或 print 出来看 |

第一行再展开说一下，因为这是最疼的：

```python
bad = {"rloe": "user", "content": "你好"}    # 创建成功，一声不响
bad["role"]                                  # 这里才炸 KeyError
```

**错在 A 点，报在 B 点**，中间隔着几十上百行代码，这就是排查时间最长的 bug。

---

## 二、class 的最小骨架

一个类，本质上就是「一份数据 + 操作这份数据的函数」，绑在一起。

```python
class Dog:
    def __init__(self, name, age):     # 造对象时自动执行
        self.name = name               # 把参数存到对象身上
        self.age = age

    def bark(self):                    # 普通方法
        return f"{self.name} 汪汪叫，它 {self.age} 岁了"

d = Dog("旺财", 3)      # 造对象，__init__ 自动被调用
d.name                  # "旺财"
d.bark()                # "旺财 汪汪叫，它 3 岁了"
```

三条必须记住：

1. **`__init__` 是造对象时自动执行的函数**，不用手动调，写 `Dog(...)` 就等于调它
2. **`self` 就是「这个对象本身」**，定义时写在第一个参数，调用时不用传，Python 自动塞
3. **`self.name = x` 是「把这个 x 存到这个对象身上」**，之后这个对象走到哪都带着它

---

## 三、`@dataclass` 省掉了什么

上面的 `Dog` 里，`__init__` 那三行纯粹是「把参数搬到 `self` 上」，毫无智力含量。字段一多，就是几十行复制粘贴。

`@dataclass` 就是把这部分交出去：

```python
from dataclasses import dataclass

@dataclass
class Dog:
    name: str
    age: int

    def bark(self):
        return f"{self.name} 汪汪叫，它 {self.age} 岁了"
```

`__init__` 不用写了，它按字段自动生成。另外还白送两个：

| 自动生成 | 作用 | 没有它的时候 |
|---|---|---|
| `__init__` | 收参数、存字段 | 得手写几十行 |
| `__repr__` | 打印成 `Message(role='user', ...)` | 打印出一串 `<object at 0x7f...>` |
| `__eq__` | 按字段值比较是否相等 | 比的是「是不是同一个对象」，永远 False |

最后那个 `__eq__` 实测对比（脚本第三节跑过）：

```python
Message("user", "hi") == Message("user", "hi")        # True   两个 dataclass
MessageByHand("user", "hi") == MessageByHand("user", "hi")   # False  手写 class
```

---

## 四、Agent 的两个零件

只有 10 行，但后面 160 天都在用它：

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Message:
    """对话历史里的一条消息。"""
    role: str          # system / user / assistant / tool
    content: str

@dataclass
class ToolCall:
    """模型提出的一次工具调用请求。"""
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
```

**为什么是两个类，不是一个 dict？** 因为它们描述的是两件不同的事：

- `Message` = **谁说了什么**（内容）
- `ToolCall` = **要做什么**（动作 + 参数）

把两者混进一个 dict，你永远分不清「content 为空」是消息本来为空，还是这条其实是工具调用。

一轮真实对话长这样：

```python
history = [
    Message(role="system",    content="你是一个简洁的助手。"),
    Message(role="user",      content="北京今天天气怎么样？"),
    Message(role="assistant", content="我查一下。"),
    Message(role="tool",      content='{"temp": 12, "desc": "多云"}'),
]

call = ToolCall(name="get_weather", arguments={"city": "北京"})
```

---

## 五、和 JSON 互转（衔接 Day6）

发给大模型的，永远是 JSON 字符串，不是你的对象。中间要过两道：

| 方向 | 做法 | 函数 |
|---|---|---|
| 对象 → JSON | 先 `asdict(m)` 变 dict，再 `json.dumps(...)` | `asdict` + `dumps` |
| JSON → 对象 | 先 `json.loads(text)` 变 dict，再 `ToolCall(**data)` | `loads` + `**` |

```python
payload = [asdict(m) for m in messages]
text = json.dumps(payload, ensure_ascii=False, indent=2)
```

反过来：

```python
raw = '{"name": "search", "arguments": {"q": "python"}}'
call = ToolCall(**json.loads(raw))       # ** 是 Day5 学的「把字典拆成关键字参数」
call.name                                 # "search"
```

**`**` 那个用法今天是第一次真正用上**。它把 `{"name": ..., "arguments": ...}` 拆成 `name=..., arguments=...` 传进去，正好对上 `__init__` 的参数名。

---

## 六、三个坑

### 坑 1：没有默认值的字段必须全传

```python
Message()      # TypeError: missing 2 required positional arguments: 'role' and 'content'
```

### 坑 2：可变默认值不能直接写 `{}`，会直接报错

```python
@dataclass
class Bad:
    args: dict = {}        # ValueError: mutable default <class 'dict'> for field args is not allowed
```

正解：

```python
args: dict = field(default_factory=dict)
```

**这个坑 Day5 见过**：`def bad(item, box=[])` 会让多次调用共享同一个列表。Python 老版本不拦你，`dataclass` 直接禁止写，等于帮你挡了一刀。

`default_factory=dict` 的意思是「每次造对象时，现场调一次 `dict()` 拿一个新的空字典」，而不是所有人共用一个。

### 坑 3：`dataclass` 不做类型检查

```python
Message(role=123, content=None)     # 照样造得出来，一声不响
```

类型注解只是**写给人看的说明**，运行时完全不检查。真要拦住，需要 Day9 的 **Pydantic**。

这也是 Day9 存在的全部理由。

---

## 七、Agent 视角：为什么框架都用类

打开任何一个 Agent 框架的源码，你都会看到类似的东西：

```python
@dataclass
class Tool:
    name: str
    description: str
    func: Callable

@dataclass
class AgentState:
    messages: list[Message]
    step: int = 0
```

原因是**模型要读你的结构**。Function Calling 时，模型看到的是：

> 工具名 `get_weather`，参数 `city: str`、`unit: str`

这些信息在 dict 里是「约定」，在类里是「强制的结构」。**你定义得多清楚，模型调用得就有多准。**

一句话带走：**Agent 的可靠性不来自模型多聪明，来自你把数据结构定义得多死。**

---

## 八、自测（三题，明天抽查）

1. `@dataclass` 自动生成了哪三个方法？各自解决什么问题？
2. 为什么 `ToolCall` 不能干脆用 `Message` 代替，多存一个 `name` 字段就行？
3. `Message(role=123, content=None)` 为什么能造出来？要拦住它得靠什么？

---

## 九、我踩的坑

（跑脚本时如果有卡住的地方，写在这）

-

## 十、一句话总结

> 参考：`dataclass` 让数据「有名字、有类型、打错字立刻报错」；`Message` 管说了什么，`ToolCall` 管要做什么；类不做类型检查，那是 Pydantic 的活。

-
