"""Day15 演示：模型是怎么从一张"概率表"里挑出下一个字的。

跑法：
    .venv\\Scripts\\python.exe -X utf8 code\\day15_sampling.py

三个演示，全本地、不联网：
  1. temperature —— 抽签有多随性（把概率表削尖 / 压平）
  2. top_p      —— 只在最靠前的几个候选里抽（先砍尾巴，再抽）
  3. 推理不学习 —— 同一个输入算 5 次，结果的"性格"不变

注意：下面的概率数字是我编的，但形式是真的 ——
真实模型每一步就是吐出一张这样的概率表，然后再抽样。
"""

import random

random.seed(7)  # 固定随机种子，保证你和我跑到一样的结果

# 模型看完「今天天气真___」之后，给出的下一字概率表
CANDIDATES = [
    ("好", 0.50),
    ("不", 0.22),
    ("挺", 0.13),
    ("还", 0.08),
    ("凑", 0.04),
    ("糟", 0.03),
]


def reweight(cands, t):
    """按温度改写概率表：T 越小越集中，T 越大越平。T=0 时只留概率最高的那个。"""
    if t <= 0:
        best = max(cands, key=lambda c: c[1])
        return [(w, 1.0 if w == best[0] else 0.0) for w, _ in cands]
    # 概率开 1/T 次方再归一化 —— 等价于"先取对数、除以温度、再softmax"
    raw = [(w, p ** (1 / t)) for w, p in cands]
    total = sum(p for _, p in raw)
    return [(w, p / total) for w, p in raw]


def apply_top_p(cands, top_p):
    """先按概率从高到低排队，累加到 top_p 就停 —— 尾巴上的候选直接砍掉。"""
    ordered = sorted(cands, key=lambda c: -c[1])
    kept, cum = [], 0.0
    for w, p in ordered:
        kept.append((w, p))
        cum += p
        if cum >= top_p:
            break
    total = sum(p for _, p in kept)
    return [(w, p / total) for w, p in kept]


def draw(cands):
    """按概率抽一次签。"""
    r = random.random()
    cum = 0.0
    for w, p in cands:
        cum += p
        if r <= cum:
            return w
    return cands[-1][0]


def show_table(label, cands):
    print(f"  {label}")
    line = "    " + "   ".join(
        f"{w} {p * 100:.0f}%" for w, p in cands if p >= 0.005
    )
    print(line)


print("=" * 58)
print("演示一：temperature —— 抽签有多随性")
print("=" * 58)
print()
print("模型看完「今天天气真___」，先给出一张下一字的概率表：")
print("    " + "   ".join(f"{w} {p * 100:.0f}%" for w, p in CANDIDATES))
print()
print("然后是 temperature 在改这张表：")
print()

for t in [0, 0.3, 0.7, 1.0, 1.5]:
    show_table(f"T = {t}", reweight(CANDIDATES, t))
    print()

print("看清楚两件事：")
print("  T=0    -> 概率全压给「好」，等于每次都选概率最高的那个 -> 每次输出都一样")
print("  T 变大 -> 冷门候选「凑」「糟」的概率被抬起 -> 更活泼，也更可能胡说")
print()
print("同一个模型、同一句话，抽 20 次，看它有多不一样：")
print()

for t in [0, 1.0, 1.5]:
    cands = reweight(CANDIDATES, t)
    counts = {}
    for _ in range(20):
        w = draw(cands)
        counts[w] = counts.get(w, 0) + 1
    parts = "  ".join(f"{w}x{n}" for w, n in counts.items())
    print(f"  T = {t:<4} {parts}")
print()
print("  -> T=0 只出一种；T 越大，出的花样越多。")
print()

print("=" * 58)
print("演示二：top_p —— 只在最靠前的几个候选里抽")
print("=" * 58)
print()

for tp in [0.5, 0.9, 1.0]:
    kept = apply_top_p(CANDIDATES, tp)
    names = "、".join(w for w, _ in kept)
    print(f"  top_p = {tp:<5} 只剩 {len(kept)} 个候选：{names}")
print()
print("  top_p=0.5 时，概率表里够了 50% 就停 —— 后面 4 个候选直接出局，")
print("  连被抽到的机会都没有。这就是它和 temperature 的分工：")
print("    temperature 管「敢不敢选冷门的」")
print("    top_p       管「冷门的还留不留在牌桌上」")
print()

print("=" * 58)
print("演示三：推理不学习")
print("=" * 58)
print()
print("同一个输入，用 T=0 连算 5 次：")
cands = reweight(CANDIDATES, 0)
outs = [draw(cands) for _ in range(5)]
print("    " + "  ".join(outs))
print()
print("  5 次全一样。但请注意 —— 这不是「它记住了上次的答案」，")
print("  而是它每次拿到同样的输入，都把同一张概率表重新算了一遍。")
print("  模型本身一个数字都没变。这就是「推理」：只算，不学。")
