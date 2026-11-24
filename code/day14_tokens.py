"""Day14 演示：模型眼里的"字"和你眼里的"字"不是一回事。

跑法：
    .venv\\Scripts\\python.exe -X utf8 code\\day14_tokens.py

两个演示，都不联网：
  1. 同一段话，用三种算法数一遍 —— 字符 / 字节 / token
  2. 模拟一个"上下文窗口"，看消息塞满之后谁会先被挤出去

注意：脚本里的 token 是**估算**（按常见规律折算），不是真实值。
真实值要用对应模型的分词器（例如 tiktoken）算，那要先下载词表，本机网络不稳，今天先不搞。
"""

# ---------- 演示一：三种数法 ----------

def count_han(text):
    """数出汉字个数。"""
    return sum(1 for c in text if "\u4e00" <= c <= "\u9fff")


def estimate_tokens(text):
    """粗略估算 token 数：汉字约 1.5 个/字，其余约 4 个字符/token。"""
    han = count_han(text)
    other = len(text) - han
    return round(han * 1.5 + other / 4)


def show(label, text):
    chars = len(text)
    byts = len(text.encode("utf-8"))
    toks = estimate_tokens(text)
    print(f"{label}")
    print(f"  原文： {text}")
    print(f"  字符数：{chars:>3}    字节数：{byts:>3}    token 估算：{toks:>3}")
    print()


print("=" * 56)
print("演示一：同一句话，三种数法")
print("=" * 56)

show("【中文 10 个字】", "北京明天天气怎么样呀")
show("【英文 10 个词】", "How is the weather in Beijing today my friend")
show("【中英混着写】", "帮我把 weather forecast 整理成表格")

print("看清楚这三行：")
print("  中文 1 个字 = 3 个字节，英文 1 个字母 = 1 个字节 —— 字节数差 3 倍")
print("  但模型既不是按字符数收费，也不是按字节数收费，是按 token")
print()

# ---------- 演示二：上下文窗口 ----------

print("=" * 56)
print("演示二：上下文窗口塞满了会怎样")
print("=" * 56)

WINDOW = 60          # 假装这个模型的窗口只能装 60 个 token
messages = []        # 对话历史：越靠前的越老

for i in range(1, 9):
    messages.append(f"第{i}轮：北京明天天气怎么样")
    total = sum(estimate_tokens(m) for m in messages)

    # 装不下了，就把最老的那条扔掉
    dropped = []
    while total > WINDOW and len(messages) > 1:
        dropped.append(messages.pop(0))
        total = sum(estimate_tokens(m) for m in messages)

    note = f"  <- 挤出去了 {len(dropped)} 条最老的" if dropped else ""
    print(f"加了第 {i} 轮后：窗口里 {len(messages)} 条，共 {total} token{note}")

print()
print(f"窗口上限是 {WINDOW} token。到最后，第 1、2 轮已经不在窗口里了——")
print("模型看不见它们，等于没说过。")
print()
print("这就是为什么聊得很长的对话，它会忘掉开头；")
print("也是为什么 Agent 不能把全部历史一直往下传，要做裁剪或摘要。")
