# Day9 第一段：不检查，会出什么事
# 目标：跑一次，亲眼看「三天」变成一长串

class WeatherArgs:
    def __init__(self, city, days):
        self.city = city
        self.days = days


a = WeatherArgs(city="北京", days="三天")

print("城市：", a.city)
print("天数：", a.days)
print("现在拿它算小时数（days * 24）：")
print(a.days * 24)
