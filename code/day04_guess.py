"""
Day4 · 猜数字（带输入校验与异常提示）

用法：
    python code/day04_guess.py

今天练的四个东西，全在这一个文件里：
    while True   主循环（不知道要跑几次 → 用 while）
    if / elif / else   大了 / 小了 / 中了
    break / continue    退出 / 跳过这次（非法输入不扣次数）
    try / except / finally   输入不是数字程序也不崩
"""

import random

LOW, HIGH = 1, 100
MAX_TRIES = 3


def play_once() -> bool:
    """玩一局。猜中返回 True，用完次数或主动退出返回 False。"""
    answer = random.randint(LOW, HIGH)
    used = 0
    print(f"\n我想好了 {LOW}~{HIGH} 之间的一个数，你有 {MAX_TRIES} 次机会（输入 q 退出）。")

    while used < MAX_TRIES:
        raw = input(f"[{used + 1}/{MAX_TRIES}] 你猜：").strip()

        # continue 的第一种用法：用户想退出
        if raw.lower() in ("q", "quit", "exit"):
            print(f"  不玩了，答案是 {answer}")
            return False

        # ---- 今天的核心：可能出错的代码放进 try ----
        # input() 拿到的是字符串，int("abc") 会抛 ValueError
        # 不接住 → 程序直接崩掉，前面猜的次数全白费
        try:
            guess = int(raw)
        except ValueError:
            print("  这串东西不是整数，重来（这次不算次数）")
            continue

        # continue 的第二种用法：范围不对，同样不扣次数
        if not LOW <= guess <= HIGH:
            print(f"  只接受 {LOW}~{HIGH} 的数字，重来（不算次数）")
            continue

        # 走到这里才算一次有效猜测
        used += 1

        if guess > answer:
            print("  大了")
        elif guess < answer:
            print("  小了")
        else:
            print(f"  中了！你用了 {used} 次。")
            return True

    print(f"  次数用完了，答案是 {answer}")
    return False


def main() -> None:
    print("=" * 44)
    print("猜数字 · Day4：控制流与异常处理")
    print("=" * 44)

    rounds = 0
    wins = 0

    try:
        while True:
            rounds += 1
            if play_once():
                wins += 1
            again = input("\n再来一局？(y 继续 / 其他任意键退出)：").strip().lower()
            if again not in ("y", "yes", "是", "好", "要"):
                break
    except KeyboardInterrupt:
        # Ctrl+C 也是一种"异常"，接住它就能优雅退出而不是满屏报错
        print("\n(检测到 Ctrl+C，安全退出)")
    finally:
        # finally 一定会执行：正常 break、return、异常、Ctrl+C 都会走到这里
        print(f"\n共玩了 {rounds} 局，赢 {wins} 局。")


if __name__ == "__main__":
    main()
