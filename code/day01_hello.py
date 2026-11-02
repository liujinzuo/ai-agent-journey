"""Day1：环境验证脚本。

目的：确认 Python 能跑、能打印、能拿到系统信息。
运行：python code/day01_hello.py
"""

import sys
import platform


def main() -> None:
    print("Hello, AI Agent!")
    print(f"Python 版本 : {sys.version.split()[0]}")
    print(f"运行平台    : {platform.system()} {platform.release()}")
    print(f"脚本路径    : {__file__}")
    print("环境通了，Day1 达成。明天开始 Day2：变量与数据类型。")


if __name__ == "__main__":
    main()
