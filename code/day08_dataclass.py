"""Day8 · 面向对象：用 dataclass 定义 Agent 的两个核心数据结构。

运行：
    python code/day08_dataclass.py

今天不追求把 OOP 学完，只求三件事：
    1. 看懂 class 的最小骨架
    2. 会用 @dataclass 定义数据类
    3. 造出 Message 和 ToolCall，并能转成 JSON
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Any


def section(title):
    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


# ---------------------------------------------------------------- 定义区

# 这就是 Day8 要交付的两个零件，只有 10 行，但后面 160 天都会用到。

@dataclass
class Message:
    """对话历史里的一条消息。"""
    role: str                    # "system" / "user" / "assistant" / "tool"
    content: str


@dataclass
class ToolCall:
    """模型提出的一次工具调用请求。"""
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)


# 对照组：用最原始的手写 class 表达同样的东西（第 3 节演示用）
class MessageByHand:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def __repr__(self):
        return f"MessageByHand(role={self.role!r}, content={self.content!r})"


# ---------------------------------------------------------------- 演示区

def part1_why():
    section("一、dict 能装数据，但挡不住打错字")

    msg = {"role": "user", "content": "你好"}
    print(f"dict 写法：{msg}")
    print(f"取值：msg['role'] -> {msg['role']}")

    print()
    print("现在把 role 拼错成 rloe：")
    bad = {"rloe": "user", "content": "你好"}
    print(f"  这个 dict 照样创建成功，没有任何报错")
    print(f"  直到你去取值才炸：", end=" ")
    try:
        bad["role"]
    except KeyError as e:
        print(f"KeyError: {e}")
    print("  → 错在写数据的地方，报在取值的地方，中间可能隔了几百行")

    print()
    print("换成 dataclass 之后：")
    print("  Message(rloe='user', content='你好') 会发生什么？", end=" ")
    try:
        Message(rloe="user", content="你好")
    except TypeError as e:
        print(f"\n  TypeError: {e}")
    print("  → 错误在创建那一刻就暴露了，这正是我们要的")


def part2_class_skeleton():
    section("二、class 的最小骨架：只有 __init__ 和 self")

    class Dog:
        # __init__ 是「造对象时自动执行的函数」，负责把数据装进对象
        def __init__(self, name, age):
            self.name = name      # self.name 是「这个对象自己的 name」
            self.age = age

        # 普通方法：第一个参数永远是 self，代表「当前这个对象」
        def bark(self):
            return f"{self.name} 汪汪叫，它 {self.age} 岁了"

    d = Dog("旺财", 3)            # 造对象：Dog.__init__ 被自动调用
    print(f"d.name      -> {d.name}")
    print(f"d.bark()    -> {d.bark()}")
    print()
    print("记住三件事：")
    print("  1. __init__ 在 Dog(...) 那一刻自动执行，不用手动调")
    print("  2. self 就是「这个对象本身」，写的时候不用传，Python 自动塞进去")
    print("  3. self.name = x 的意思是「把这个 x 存到这个对象身上」")


def part3_dataclass():
    section("三、@dataclass：把 __init__ 这类样板代码交出去")

    # 手写版和 dataclass 版，做的事情一模一样
    hand = MessageByHand("user", "你好")
    auto = Message("user", "你好")

    print(f"手写 class：{hand}")
    print(f"dataclass ：{auto}")
    print()
    print("两行 @dataclass 帮你自动生成了三样东西：")
    print("  __init__  造对象时自动收参数、存字段")
    print("  __repr__  打印对象时显示成 Message(role='user', ...) 而不是一串内存地址")
    print("  __eq__    两个对象比较时按字段值比较，而不是比内存地址")
    print()
    print(f"两个 Message 内容相同，相等吗？ {Message('user', 'hi') == Message('user', 'hi')}")
    print(f"用手写 class 呢？             {MessageByHand('user', 'hi') == MessageByHand('user', 'hi')}")
    print("  → 手写版没写 __eq__，比的是「是不是同一个对象」，所以是 False")


def part4_agent_parts():
    section("四、造出 Agent 的两个零件")

    m1 = Message(role="system", content="你是一个简洁的助手。")
    m2 = Message(role="user", content="北京今天天气怎么样？")
    call = ToolCall(name="get_weather", arguments={"city": "北京", "unit": "celsius"})
    m3 = Message(role="assistant", content="我查一下。")
    m4 = Message(role="tool", content='{"temp": 12, "desc": "多云"}')

    history = [m1, m2, m3, m4]

    print("一轮完整的对话历史：")
    for i, m in enumerate(history, 1):
        print(f"  {i}. [{m.role:9s}] {m.content}")

    print()
    print(f"模型要求调用工具：{call.name}")
    print(f"参数：{call.arguments}")
    print()
    print("注意：Message 是「说了什么」，ToolCall 是「要做什么」，两者分开。")
    print("这就是为什么框架里它们是两个类，而不是塞进一个 dict 里。")


def part5_to_json():
    section("五、转成 JSON —— 和大模型通信时就是这么发的")

    messages = [
        Message(role="system", content="你是一个简洁的助手。"),
        Message(role="user", content="北京天气？"),
    ]

    payload = [asdict(m) for m in messages]
    text = json.dumps(payload, ensure_ascii=False, indent=2)

    print("asdict() 把一个 Message 变成普通 dict：")
    print(f"  {asdict(messages[1])}")
    print()
    print("再用 Day6 学过的 dumps 变成字符串（这就是发给 API 的格式）：")
    print(text)

    print()
    print("反过来，从 API 收到的 JSON 也能还原成对象：")
    raw = '{"name": "search", "arguments": {"q": "python dataclass"}}'
    data = json.loads(raw)
    call = ToolCall(**data)          # ** 是 Day5 学的「把字典拆成关键字参数」
    print(f"  json.loads 得到：{data}")
    print(f"  ToolCall(**data) 得到：{call}")
    print(f"  现在可以用属性访问了：call.name = {call.name!r}")


def part6_pitfall():
    section("六、三个坑（后两个是 dataclass 的脾气）")

    print("坑 1：字段没有默认值时，必须全部传")
    try:
        Message()
    except TypeError as e:
        print(f"  Message() -> TypeError: {e}")

    print()
    print("坑 2：可变默认值不能直接写 {}，编译器会拦你")
    try:
        @dataclass
        class Bad:
            args: dict = {}
    except ValueError as e:
        print(f"  报错原文：{e}")
        print("  正解：arguments: dict = field(default_factory=dict)")
        print("  → 还记得 Day5 那个 def bad(item, box=[]) 吗？同一个坑，")
        print("    dataclass 直接不让写，帮你挡住了。")

    print()
    print("坑 3：dataclass 不做类型检查")
    wrong = Message(role=123, content=None)
    print(f"  Message(role=123, content=None) 照样能造出来：{wrong}")
    print("  → 类型注解只是「说明」，运行时不管。真要拦住，得等 Day9 的 Pydantic。")


def main():
    print("Day8 · 面向对象：从 dict 到 dataclass")
    part1_why()
    part2_class_skeleton()
    part3_dataclass()
    part4_agent_parts()
    part5_to_json()
    part6_pitfall()

    print()
    print("=" * 64)
    print("跑完了。今天只求记住一句：")
    print("  dataclass 让你的数据「有名字、有类型、打错字立刻报错」。")
    print("  Agent 里的 Message、ToolCall、Tool、State，全都是这么定义的。")
    print("=" * 64)


if __name__ == "__main__":
    main()
