"""Day5 验收：自动比对「重构版」和「原版」的输出是否一字不差。

为什么要有这个文件：
    靠眼睛看两段输出一样不一样，是不可靠的 —— 少一个空格、多一个小数位都看不出来。
    验收要用程序对着比：输入同一组数据，逐字节比较。

运行：python code/day05_verify.py
"""

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent

# 三组输入：普通整数、除不尽、小数
CASES = [("10", "3"), ("7", "2"), ("1.5", "0.5")]


def run(script: str, inputs: tuple) -> tuple[str, int]:
    """用同一组输入跑一个脚本，返回（标准输出, 返回码）。"""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, str(HERE / script)],
        input="\n".join(inputs) + "\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return proc.stdout.strip(), proc.returncode


def main() -> None:
    print("=" * 56)
    print("Day5 验收：重构版  vs  原版")
    print("=" * 56)

    all_ok = True
    for inputs in CASES:
        old, rc_old = run("day02_calculator.py", inputs)
        new, rc_new = run("day02_calculator_func.py", inputs)
        ok = old == new and rc_old == 0 and rc_new == 0
        all_ok = all_ok and ok

        print(f"\n输入 {inputs[0]} 和 {inputs[1]}")
        print(f"  结果：{'一致 [OK]' if ok else '不一致 [待修]'}")
        if not ok:
            print(f"  原版（返回码 {rc_old}）：\n{old}")
            print(f"  新版（返回码 {rc_new}）：\n{new}")

    print("\n" + "=" * 56)
    if all_ok:
        print("三组输入全部一致，Day5 的重构验收通过。")
    else:
        print("有差异，看上面的对照。最常见的原因：f-string 里空格或小数格式不同。")
    print("=" * 56)


if __name__ == "__main__":
    main()
