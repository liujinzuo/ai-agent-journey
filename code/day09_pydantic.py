# Day9 第二段：请一位检查员
# 目标：跑一次，看到它拦下来、说清楚哪里错、填对了就放行
# 说明：外面这层 try 只是为了让两种结果一次看完，你可以先不管它

from pydantic import BaseModel, ValidationError


class WeatherArgs(BaseModel):
    city: str
    days: int


print("===== 第一次：故意填错（days 给了「三天」）=====")
try:
    a = WeatherArgs(city="北京", days="三天")
    print("居然通过了：", a)
except ValidationError as e:
    print("被拦下来了，报错原文：")
    print(e)

print()
print("===== 第二次：填对（days 给 3）=====")
b = WeatherArgs(city="北京", days=3)
print("通过了：", b)
print("算小时数：", b.days * 24)
