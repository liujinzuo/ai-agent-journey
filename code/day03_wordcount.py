"""
Day3 · 词频统计 Top 20

用法：
    python code/day03_wordcount.py                 # 默认读 code/sample.txt
    python code/day03_wordcount.py 别的文件.txt     # 读指定文件

一条数据流，正好把 Day3 的四种结构全用上：

    文件(str) --清洗--> 单词(list) --计数--> 词频(dict) --排序--> Top20(list[tuple])
"""

import sys
from pathlib import Path

# 停用词：出现频率极高但没有信息量的词，先过滤掉，否则 Top20 全是 the / and / of
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "at", "for",
    "is", "are", "was", "were", "be", "been", "it", "its", "this", "that",
    "with", "as", "by", "from", "not", "you", "your", "we", "our", "they",
    "can", "will", "if", "what", "then", "than", "so", "do", "does", "has",
    "have", "had", "more", "most", "up", "out", "into", "about", "when",
}


def load_text(path: Path) -> str:
    """读文件。read_text 一步搞定，encoding 必须显式写 utf-8。"""
    return path.read_text(encoding="utf-8")


def clean_words(text: str) -> list[str]:
    """文本 -> 干净的单词列表。

    两步：
    1) 去标点：非字母字符一律换成空格（"agent." -> "agent "）
    2) 切分 + 转小写 + 丢停用词 + 丢单字母碎片（don't 会被切成 don + t，t 丢掉）
    """
    replaced = []
    for ch in text:
        replaced.append(ch if ch.isalpha() else " ")
    raw = "".join(replaced).lower().split()
    return [w for w in raw if w not in STOPWORDS and len(w) >= 2]


def count_words(words: list[str]) -> dict[str, int]:
    """list -> dict 计数，字典最经典的用法：键是单词，值是次数。

    counts.get(w, 0) 这一行是今天最该记住的：
    键不存在时返回 0，而不是抛 KeyError。
    """
    counts: dict[str, int] = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts


def top_n(counts: dict[str, int], n: int = 20) -> list[tuple[str, int]]:
    """dict -> 排好序的 list[tuple]。

    counts.items() 把字典变成 [(单词, 次数), ...]
    key=lambda kv: kv[1] 表示按第 2 项（次数）排序
    reverse=True 表示从大到小
    """
    return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:n]


def main() -> None:
    default = Path(__file__).with_name("sample.txt")
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default

    if not path.exists():
        print(f"[!] File not found: {path}")
        print("    Usage: python code/day03_wordcount.py [file.txt]")
        return

    words = clean_words(load_text(path))
    counts = count_words(words)
    ranking = top_n(counts, 20)

    print(f"File : {path.name}")
    print(f"Words: {len(words)} total, {len(counts)} unique")
    print("Top 20:")
    print("-" * 46)

    max_count = ranking[0][1] if ranking else 1
    for i, (word, c) in enumerate(ranking, start=1):
        bar = "#" * max(1, round(c / max_count * 24))
        print(f"{i:>3}. {word:<14} {c:>3}  {bar}")

    print("-" * 46)
    print("Done. counts is just a dict - same shape as a JSON object.")


if __name__ == "__main__":
    main()
