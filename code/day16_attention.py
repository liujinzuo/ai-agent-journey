"""Day16 演示：模型读一句话时，到底在看哪儿。

跑法：
    .venv\\Scripts\\python.exe -X utf8 code\\day16_attention.py

三个演示，全本地、不联网：
  1. 只看"有哪些词"，分不清「狗咬人」和「人咬狗」
  2. 注意力：让「它」自己挑它到底在看谁 —— 两句话，答案相反
  3. 座位号：给每个词贴一个位置编号，顺序就进得去了

注意：下面的"关注分数"是我编的，但形式是真的 ——
真实模型里，每两个词之间都会算一个分数，再归一化成百分比。
"""

import math
from collections import Counter


def bag(sentence):
    """把句子拆成"词 + 出现几次"，顺序信息就丢掉了。"""
    return Counter(sentence.split())


def softmax(scores):
    """把一堆任意大小的分数变成加起来等于 1 的百分比。"""
    m = max(scores.values())          # 先减最大值，防止 e 的指数太大炸掉
    exps = {w: math.exp(s - m) for w, s in scores.items()}
    total = sum(exps.values())
    return {w: e / total for w, e in exps.items()}


def show_attention(target, scores):
    print(f"  「{target}」在看谁：")
    probs = softmax(scores)
    for w, p in sorted(probs.items(), key=lambda x: -x[1]):
        bar = "█" * max(1, round(p * 40))
        print(f"    {w}{'　' * (4 - len(w))} {p * 100:5.1f}%  {bar}")
    print()


print("=" * 60)
print("演示一：只有词、没有顺序，会怎样")
print("=" * 60)
print()

a = "狗 咬 人"
b = "人 咬 狗"

print(f"  句子A：{a}")
print(f"  句子B：{b}")
print(f"  A 的词袋：{dict(bag(a))}")
print(f"  B 的词袋：{dict(bag(b))}")
print(f"  两个词袋一样吗？{bag(a) == bag(b)}")
print()
print("  意思完全相反，词袋却一模一样 —— 因为数词的时候把顺序扔了。")
print("  所以模型光知道「句子里有狗、有咬、有人」是不够的。")
print()

print("=" * 60)
print("演示二：注意力 —— 让每个词自己去挑该看谁")
print("=" * 60)
print()

sentence_a = "小猫 没有 跳过 栅栏 因为 它 太 累 了"
sentence_b = "小猫 没有 跳过 栅栏 因为 它 太 宽 了"

print(f"  句子A：{sentence_a}")
show_attention(
    "它",
    {"小猫": 4.0, "累": 2.0, "跳过": 0.4, "栅栏": 0.3, "太": 0.2, "没有": 0.1, "因为": 0.1, "了": 0.1},
)

print(f"  句子B：{sentence_b}")
show_attention(
    "它",
    {"栅栏": 4.0, "小猫": 1.2, "跳过": 0.6, "太": 0.2, "没有": 0.1, "因为": 0.1, "了": 0.1},
)

print("  同一个「它」，两句话里指向完全不同的东西：")
print("    A 里「它」≈ 小猫（累了才没跳）")
print("    B 里「它」≈ 栅栏（太宽了才没跳）")
print("  没有人写这条规则。是模型拿「它」和每个词算了一遍相关性。")
print()
print("  这就是「注意力」：每个词给全句每个词打一个分，")
print("  分越高 = 越相关 = 从它那儿拿的信息越多。")
print()

print("=" * 60)
print("演示三：座位号 —— 顺序是怎么进去的")
print("=" * 60)
print()

for i, w in enumerate(a.split(), 1):
    print(f"    位置 {i}：{w}")
print()
for i, w in enumerate(b.split(), 1):
    print(f"    位置 {i}：{w}")
print()
print("  词一样，座位号不一样：「狗」在 A 坐 1 号，在 B 坐 3 号。")
print("  模型看到的不是一个词袋，而是「词 + 它在第几位」。")
print("  这个座位号就是「位置编码」。")
print()
print("  三件事串起来，就是 Transformer 干的事：")
print("    每个词 -> 算它和全句各词的相关性 -> 按相关性把别人的信息捞过来 -> 再往下传")
print("    一层层重复几十次，最后才轮到「猜下一个字」。")
