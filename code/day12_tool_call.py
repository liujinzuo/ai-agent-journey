# Day12 · 模型只点菜，不下厨
# 目标：跑一遍，看清楚「模型说要调工具」到「工具真的执行」中间发生了什么
# 注意：这里没有联网，第 ③ 步的「模型回复」是我写死的，真实情况由 API 返回

import json

from pydantic import BaseModel

# ① 菜单：你要递交给模型的「可用工具清单」
TOOLS = [
    {
        "name": "get_weather",
        "description": "查某个城市未来几天的天气",
        "parameters": {"city": "城市名", "days": "天数，整数，默认 1"},
    }
]


# ② 厨房：真正干活的那个普通函数
def get_weather(city, days=1):
    return f"{city} 未来 {days} 天都是晴，18~25 度"


# ③ 模型看过菜单后，回给你的东西（真实情况是 API 返回的 JSON）
model_reply = '{"name": "get_weather", "arguments": {"city": "北京", "days": 3}}'


# ④ 检查关口（Day9 学的）
class WeatherArgs(BaseModel):
    city: str
    days: int = 1


print("== 第 1 步：递给模型的菜单 ==")
print(json.dumps(TOOLS, ensure_ascii=False, indent=2))

print("\n== 第 2 步：模型点菜（它没回答问题，只说要用哪个工具）==")
print(model_reply)

print("\n== 第 3 步：你的程序验菜 ==")
call = json.loads(model_reply)
args = WeatherArgs(**call["arguments"])
print("要调用的工具：", call["name"])
print("参数检查通过：", args)

print("\n== 第 4 步：你的程序下厨 ==")
result = get_weather(args.city, args.days)
print("工具返回：", result)

print("\n== 第 5 步：把菜端回模型，它才会回答用户 ==")
print(f"（下一轮发给模型的内容：工具 get_weather 返回了「{result}」）")
