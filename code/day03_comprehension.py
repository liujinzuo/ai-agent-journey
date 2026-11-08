"""Day3 补课 · 列表推导式 / 字典推导式（10 分钟）

跑法：python code/day03_comprehension.py
规则：先跑一遍看输出，再去改最下面「练习区」的两个 TODO，改完再跑，
      自检会告诉你通过还是待修。
"""

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
words = ["agent", "tool", "model", "loop"]
counts = {"agent": 5, "tool": 3, "model": 2}

print("=" * 52)
print("示例 1 · 普通循环 vs 推导式（同一件事，两种写法）")
squares_loop = []
for n in nums:
    squares_loop.append(n * n)
squares_comp = [n * n for n in nums]
print("  循环  :", squares_loop)
print("  推导式:", squares_comp)
print("  一样吗:", squares_loop == squares_comp)

print("\n示例 2 · 带条件 if（只要偶数）")
evens = [n for n in nums if n % 2 == 0]
print("  [n for n in nums if n % 2 == 0] ->", evens)

print("\n示例 3 · 带 if...else（每个都要，但分两种处理）")
labels = ["偶" if n % 2 == 0 else "奇" for n in nums]
print("  结果:", labels)
print("  注意：if 在前是「过滤」，if...else 在后是「二选一」，位置不同含义完全不同")

print("\n示例 4 · 字符串处理（转大写 / 算长度）")
print("  [w.upper() for w in words] ->", [w.upper() for w in words])
print("  [len(w) for w in words]    ->", [len(w) for w in words])

print("\n示例 5 · 字典推导式（把 单词->次数 翻成 次数->单词）")
flip = {v: k for k, v in counts.items()}
print("  原:", counts)
print("  翻:", flip)
print("  写法读作：对每个 k,v，产出 v:k")

print("\n示例 6 · 真实用途：用推导式改写 day03_wordcount.py 里的清洗")
STOPWORDS = {"the", "a", "is", "of"}
raw = ["The", "agent", "is", "a", "tool", "of", "agent"]
clean_loop = []
for w in raw:
    w = w.lower()
    if w not in STOPWORDS:
        clean_loop.append(w)
clean_comp = [w.lower() for w in raw if w.lower() not in STOPWORDS]
print("  循环  :", clean_loop)
print("  推导式:", clean_comp)
print("  一样吗:", clean_loop == clean_comp)
print("  => 你 Day3 脚本里那 4 行，可以压成这 1 行")


# ============================================================
# 练习区：改这里的两个 TODO，改完再跑一次，看下面的自检
# ============================================================

# 练习 1：用推导式，把 nums 里的偶数挑出来，放进 evens_mine
#   提示：[n for n in nums if n%2=0]
evens_mine = [n for n in nums if n % 2 == 0]
      # TODO 改这一行

# 练习 2：用推导式，把 words 里每个词后面加个 "s"，放进 plural
#   提示：[w + "s" for w in words]
plural = [w + "s" for w in words]
           # TODO 改这一行

# 练习 3（可选，稍难）：用字典推导式，把 counts 里的次数都翻倍
doubled = {k: v * 2 for k, v in counts.items()}


# ============================================================
# 自检（不用改，只看结果）
# ============================================================

def check(name, got, want):
    if got == want:
        print(f"  [OK]   {name}")
    else:
        print(f"  [待修] {name}\n         现在得到：{got}\n         应该是  ：{want}")


print("\n" + "=" * 52)
print("自检")
check("练习1 偶数", evens_mine, [2, 4, 6, 8, 10])
check("练习2 加 s", plural, ["agents", "tools", "models", "loops"])
check("练习3 次数翻倍", doubled, {"agent": 10, "tool": 6, "model": 4})

passed = (
    evens_mine == [2, 4, 6, 8, 10]
    and plural == ["agents", "tools", "models", "loops"]
    and doubled == {"agent": 10, "tool": 6, "model": 4}
)
print("\n" + ("全部通过，Day3 的推导式这条补完了 ✅" if passed
              else "还有待修的，对着「应该是」那行改一下，3 分钟内能搞定。"))
