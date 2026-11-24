# Day10 第二段：聪明办法——三壶一起烧
# 目标：同样是三壶茶，看总共用了几秒

import asyncio
import time


async def make_tea(name):
    print(f"{name}：开始烧水")
    await asyncio.sleep(1)   # 这 1 秒让出去，别人先干
    print(f"{name}：茶好了")


async def main():
    start = time.time()
    await asyncio.gather(
        make_tea("第一壶"),
        make_tea("第二壶"),
        make_tea("第三壶"),
    )
    print(f"总共用了 {time.time() - start:.1f} 秒")


asyncio.run(main())
