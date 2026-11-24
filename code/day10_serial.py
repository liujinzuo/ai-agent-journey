# Day10 第一段：笨办法——一壶一壶烧
# 目标：跑一次，记住总共用了几秒

import time


def make_tea(name):
    print(f"{name}：开始烧水")
    time.sleep(1)          # 干等 1 秒，人站在旁边什么都不做
    print(f"{name}：茶好了")


start = time.time()
make_tea("第一壶")
make_tea("第二壶")
make_tea("第三壶")
print(f"总共用了 {time.time() - start:.1f} 秒")
