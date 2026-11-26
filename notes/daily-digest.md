# AI Agent 学习简记 · Day1~Day12

> 一天一节，每学完一天往下追加一节。
> 每节只有三样东西：**4 个字的小标题**、**3 句要点**、**当天最关键的几行代码**。
> 想不起某天的细节，回仓库翻 `notes/DayXX.md`。

---

## Day1 · 装台子（2026-11-02）

1. 装齐四样：Python 3.13、Git、VS Code、项目虚拟环境 `.venv`。
2. 仓库 `ai-agent-journey` 建好，`git init / add / commit / push` 走通一遍。
3. 第一行代码跑通、第一次 push 成功，地基就算打完。

```python
print("hello agent")
```

> 记忆锚：**工具装齐，第一行跑通。**

---

## Day2 · 存数据（2026-11-03）

1. 变量不是盒子，是**贴在值上的标签**——重新赋值等于换标签。
2. 四种基本类型：`int` / `float` / `str` / `bool`，`type()` 能查。
3. `input()` 拿回来的**永远是字符串**，要算数必须先 `float()` 转换。

```python
age = float(input("你几岁："))   # 不转就是字符串
print(f"明年你 {age + 1} 岁")     # f-string 把变量塞进句子
```

> 记忆锚：**输入进来是字符串，要算数先转换。**

---

## Day3 · 装盒子（2026-11-04）

1. 列表有序能改、字典按键取值、元组不能改、集合去重——**Agent 里 90% 的时间在列表和字典上**。
2. 计数万能一行：`counts.get(w, 0) + 1`。
3. 推导式模板：`[产出 for 变量 in 来源 if 条件]`，一行顶一个循环。

```python
text = "agent tool agent model agent"
counts = {}
for w in text.split():
    counts[w] = counts.get(w, 0) + 1      # 计数万能一行
print([w for w, n in counts.items() if n > 1])   # 推导式：只要出现多次的
```

> 记忆锚：**一次装一堆，按键取一个。**

---

## Day4 · 会判断（2026-11-05）

1. `if / elif / else` **从上往下只走第一个成立的**；判断相等用 `==`，`=` 是赋值。
2. `break` 结束整个循环，`continue` 只跳过这一次。
3. `try / except` 让程序出错不崩——**异常是给程序看的，错误信息才是给模型看的**。

```python
try:
    n = float(raw)
except ValueError:
    n = None          # 不崩，交回一个「读不出来」的信号
```

> 记忆锚：**会分岔、会转圈、出错不崩。**

---

## Day5 · 包名字（2026-11-10）

1. `def` 把一段活包起来，`return` 把结果交出去——**没有 `return` 的函数返回 `None`**。
2. 默认参数写在后面，`*args` 收多余的位置参数，`**kwargs` 收多余的关键字参数。
3. `if __name__ == "__main__":` 的意思是「只有直接运行这个文件时才执行这段」。

```python
def calculate(a, b, op="+"):
    if op == "+":
        return a + b
    if op == "/":
        return a / b

print(calculate(10, 3))        # 13.0，用了默认的 +
```

> 记忆锚：**一段活包成名字，起名之后随时喊。**

---

## Day6 · 数据不丢（2026-11-11）

1. 路径用 `Path(__file__).parent / "todo.json"`——**永远按脚本位置找文件**，不受在哪运行影响。
2. `json.dump` 存、`json.load` 读，中文必须 `ensure_ascii=False`，否则变乱码。
3. 写文件先写 `.tmp` 再 `replace`——中途崩溃也不会把原数据写坏。

```python
DATA = Path(__file__).parent / "todo.json"

def save(todos):
    tmp = DATA.with_suffix(".tmp")
    tmp.write_text(json.dumps(todos, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(DATA)      # 原子替换，不怕中途断电
```

> 记忆锚：**关掉程序，数据还在。**

---

## Day7 · 串一遍（2026-11-13）

1. 这天不学新东西，只做复盘：把 Day1~Day6 的散点连成一条线。
2. 填完 `Week01-review.md`，写了周记，做了 12 题自测。
3. **复盘不是重学，是给自己建索引**——以后回想靠索引，不靠记忆。

> 记忆锚：**回头看，把散的连成线。**

---

## Day8 · 定形状（2026-11-15）

1. 字典拼错键不报错、要等用的时候才炸；class 让「错在写的地方就报」。
2. `@dataclass` 自动生成 `__init__` / `__repr__` / `__eq__`——省下的不是行数，是**漏写的可能性**。
3. **类型注解运行时不检查**：`Message(role=123)` 造得出来，一声不响。

```python
@dataclass
class ToolCall:
    name: str
    arguments: dict = field(default_factory=dict)

call = ToolCall(name="get_weather", arguments={"city": "北京"})
```

> 记忆锚：**给数据起名字、定形状，形状错了立刻报。**

---

## Day9 · 有人把关（2026-11-15）

1. 类型注解是**印在表格上的要求，纸不会自己看**；Pydantic 是站在收表处的人。
2. 不检查的后果不是报错，是给你一个荒唐结果继续跑——`"三天" * 24` 会复制 24 遍字符串。
3. 换成 `class X(BaseModel)` 且不写 `__init__`，填错当场退回，并指名**哪个栏位、该怎么填**。

```python
class WeatherArgs(BaseModel):
    city: str
    days: int = 1

WeatherArgs(city="北京", days="三天")   # ValidationError: days 要整数
```

> 记忆锚：**它能猜出意思的（"3"）帮你转，猜不出的（"三天"）才拦。**

---

## Day10 · 别干站着（2026-11-15）

1. 串行烧三壶水 3 秒，三壶一起点 1 秒——**等待不是干活，浪费它就是浪费程序**。
2. `time.sleep` 堵住整个程序；`await asyncio.sleep` 把这段时间让给别人。
3. **并发不让单件事变快**，只省掉干站着的部分；后一件依赖前一件时，只能串行。

```python
async def make_tea(name):
    await asyncio.sleep(1)      # 让出去，别人先干

await asyncio.gather(make_tea("A"), make_tea("B"), make_tea("C"))
```

> 记忆锚：**互不依赖就一起派出去，有依赖就老实排队。**

---

## Day11 · 说清楚话（2026-11-16）

1. 提示词四件套：**角色 / 任务 / 约束 / 输出格式**，四样齐了再发。
2. 模型默认会「多说一点」，不写「不要解释」它就解释；这些对人贴心，对程序是灾难。
3. **格式管「要什么样」，约束管「不许干什么」**——只说「别乱加装饰」，师傅仍不知道要做成什么样。

```text
你是财务助理。
任务：把下面 6 笔支出整理成表格。
约束：不要解释，不要开场白，不要自己加项目。
输出格式：Markdown 表格，两列（用途 / 金额（元）），金额保留两位小数。
```

> 记忆锚：**模型不会读心，要求说到多细，它就能做到多准。**

---

## Day12 · 只点菜（2026-11-17）

1. 模型**不执行任何代码**，它只输出「用哪个工具、参数填什么」——像顾客点菜，不进厨房。
2. 一次工具调用实际是**问模型两次**：第一次点菜，你的程序做完，把结果端回去，它才开口回答。
3. 模型看不见你的代码，只看得见你递的**菜单**（工具清单）；菜单写得糙，它就点错菜。

```python
TOOLS = [{"name": "get_weather",
          "description": "查某个城市未来几天的天气",
          "parameters": {"city": "城市名", "days": "天数，整数"}}]

model_reply = '{"name": "get_weather", "arguments": {"city": "北京", "days": 3}}'
args = WeatherArgs(**json.loads(model_reply)["arguments"])   # 闸门先验
result = get_weather(args.city, args.days)                    # 你的代码才动手
```

> 记忆锚：**模型只点菜，一口锅都碰不到。**

---

## Day13 · 发请求（2026-11-18）

1. 程序「问模型」就是寄**一个包裹**：收件地址（URL）+ 门禁卡（API key）+ 内容（一段 JSON），换回一张回执（状态码 + JSON）。
2. 所有模型 API 形状都一样；地址和字段名不同，寄包裹的动作不变——今天跑本地假服务器，明天换真地址即可。
3. **4 开头的错在自己，5 开头的错在对方**：401 是钥匙没带对，别去改代码；429 是问太快；500 是对面出问题。
4. 钥匙三铁律：不写进代码、不截图、不进 git（放 `.env`，把 `.env` 写进 `.gitignore`）。

```python
headers = {"Content-Type": "application/json",
           "Authorization": f"Bearer {sk}"}          # 钥匙放头部，不放代码里
req = Request(url, data=json.dumps(body).encode("utf-8"),
              headers=headers, method="POST")
with urlopen(req) as resp:                            # 回执：状态码 + 内容
    data = json.loads(resp.read().decode("utf-8"))
```

> 记忆锚：**地址、钥匙、内容——三样寄过去，回执回来。**

---

## Day14 · 按块算（2026-11-19）

1. 模型不按「字」读你的话，按**块（token）**读：英文约 4 字母 / 中文约 1~2 字一块；它按块看、按块记、按块收钱。
2. 反直觉：中文 10 字 ≈ 15 token，英文 45 字母 ≈ 11 token——**同样的意思中文更贵**，因为中文常用词切得碎。
3. **上下文窗口**有上限，超出的部分不是"忘了"，是**根本没被读**；聊久了忘开头、纠正过又犯，都是这一条。
4. 幻觉不是"记性差"，是另一种病：它只有"猜"、没有"查"，不知道就编一个通顺的。

```python
# 关键信息不交给对话历史，永远放在最前面或每轮重新注入
messages = [
    {"role": "system", "content": "该用户是 VIP，等级：金卡"},   # 不会被挤掉
    *recent_turns,                                              # 只有最近几轮
    {"role": "user", "content": "我的订单到哪了"},
]
```

> 记忆锚：**重要的东西每次都给，不要指望它记得。**

---

## Day15 · 掷骰子（2026-11-21）

1. 模型不是先想好整句再写：它算出一张「下一个字可能是什么」的概率表，**按表抽签**，抽完接到句尾再抽下一次。
2. temperature 是插在「原始分数」和「取指数」之间的一步除法——分差被放大就更确定，被缩小就更发散；**只有 0 才是不抽签**，0.2 仍在抽，只是极少抽到冷门。
3. 它学说话叫**预训练**（几个月、改模型本身，学完就冻住），每次调用叫**推理**（现算一遍、不改模型）——所以你的纠正只活在这次窗口里。

```python
def reweight(cands, t):                            # 温度 = 分数先除以它
    raw = [(w, p ** (1 / t)) for w, p in cands]    # 等价于 logits/T 再 softmax
    total = sum(p for _, p in raw)
    return [(w, p / total) for w, p in raw]
# 2 分 vs 1 分两个候选：T=0.5 -> 88%/12%，T=1 -> 73%/27%，T=2 -> 62%/38%
```

> 记忆锚：**只有 0 是停止随机的开关，其余都还在抽签。**

---

## Day16 · 回头看（2026-11-22）

1. 只数词不够：「狗咬人」和「人咬狗」的词袋一模一样，顺序一扔，意思就没了。
2. **注意力** = 每个词跟全句每个词算相关性分数再归一化：「它」在「太累了」里指向小猫 79%，在「太宽了」里指向栅栏 85%——没有规则，全是算出来的。
3. 纯注意力本身分不清前后，要靠**位置编码**给每个词贴座位号；叠几十层之后，才轮到猜下一个字。Q/K/V 和矩阵推导一概不用碰。

```python
def softmax(scores):                      # 一堆分数 -> 加起来等于 1 的百分比
    m = max(scores.values())              # 先减最大值，防止 e 的指数炸掉
    exps = {w: math.exp(s - m) for w, s in scores.items()}
    total = sum(exps.values())
    return {w: e / total for w, e in exps.items()}
```

> 记忆锚：**注意力找谁相关，预训练决定凭什么相关。**

---

## Day17 · 自己发请求（2026-11-24）

1. 钥匙只放 `.env`：`.gitignore` 挡住 `.env`、放行 `.env.example`，所以模板能进仓库、真钥匙进不去。代码里只从文件读，绝不写死。
2. 回执是一大段 JSON，只有三处要用：`choices[0].message.content` 是它说的话，`finish_reason` 是为什么停（`stop` 说完了 / `length` 被截断），`usage` 是花了多少 token。
3. **解析之前先看 `finish_reason`**：不是 `stop` 就去处理，别硬解析半截 JSON——这个习惯能省几十次排查。

```python
req = urllib.request.Request(
    API_URL,
    data=json.dumps({"model": MODEL, "messages": msgs, "temperature": 0}).encode(),
    headers={"Authorization": f"Bearer {key}"},   # 钥匙只在头部，不进代码
    method="POST",
)
with urllib.request.urlopen(req, timeout=60) as resp:
    reply = json.loads(resp.read().decode())
```

> 记忆锚：**先看 finish_reason，再解析 content。**

---

## Day18 · 说清楚（2026-11-25）

1. 你写的不是「问题」，是「订单」：**角色**（谁做）、**任务**（做什么）、**约束**（不许怎样）、**格式**（交成什么样）。写不清，它就交它自己觉得好的那种。
2. 四版递进实测：裸问给散文、只给任务给中文列表，**两版都解析失败**；一加 JSON 骨架立刻能读。**格式是最硬的一条，角色是最弱的一条**——写了「你是客服工单助手」但没定格式，照样给人话。
3. 约束是双刃剑：加了「没明确写出的填 null」后，「不给退我就去投诉」被判成 null（只写了后果，没写要求），换成「我要退钱」立刻是 true。**判定看字面有没有那个动作，不替客户补心思。**

```python
system = (
    "你是客服工单助手。"                                    # 角色
    "只输出一个 JSON 对象，不要 markdown 代码块，不要解释。"   # 格式 + 不许加什么
    "issue_type 只能是：物流 / 质量 / 退款 / 其他。"           # 枚举，把自由发挥关进笼子
    "消息里没有明确写出的信息一律填 null，绝对不要猜。"         # 约束，防编造
)
```

> 记忆锚：**不要问它「说了什么」，要规定它「交什么」。**

---

## Day19 · 放大规则（2026-11-26）

1. 示例单看无害：同一条消息，严格规则下不带示例判 `true`、带示例判 `null`；可再加一条 false 示例（一变两条）**还是 `null`** —— 说明不是「示例太少」。2×2 摆开只坏一格：**严格规则 + 示例同时在场**才出事。
2. 所以示例不是教程而是放大器：规则写了「没明说就 null」，它就多了一个随时能退的出口；示例一在场，判据就从「有没有这个诉求」变成「像不像这一条」。修法不是改示例，是**把松紧拆到字段上**：`order_id` 死守原文、`refund_requested` 按诉求判。
3. 让它先写一行「依据」再给 JSON（思维链），结论会跟着理由走，错了也能一眼看出哪一步想歪。代价：输出翻倍、格式变脏，代码只能抓最后一个 `{...}`，不能整段 `json.loads`。

```python
# 松紧拆到字段上：不同字段允许不同严格度
"- order_id：必须能在原文里找到完整单号原文；找不到就填 null，绝不允许补全或编造。\n"
"- refund_requested：明确提出「要退 / 要退钱 / 要退款 / 要退货」填 true；\n"
"  只抱怨、威胁投诉、追问进度但没提退款填 false；完全没涉及退款才填 null。\n"
```

> 记忆锚：**示例不改规则，只放大规则。**
