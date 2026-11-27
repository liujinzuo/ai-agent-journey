# Day20 · 事前约束（结构化输出）

> Day18~19 你一直在做同一件事：模型交一坨文字，你的代码在旁边抠 JSON。
> 今天把方向倒过来——**先规定它必须交什么，抠的动作就不需要了。**

跑法：

```powershell
cd C:\Users\22155\ai-agent-journey
.venv\Scripts\python.exe -X utf8 code\day20_json_mode.py
```

四站加一次重试，共六次调用，不到一分钱。

---

## 一、先看 DeepSeek 到底支持到哪一档

这是今天所有写法的前提，实测结果：

| 请求方式 | 结果 | 保证了什么 |
|---|---|---|
| 不加 `response_format` | 能返回 JSON | 什么都不保证 |
| `{"type": "json_object"}` | 正常返回，是合法 JSON | **只保证能被 `json.loads`** |
| `{"type": "json_schema", ...}` | `HTTP 400：This response_format type is unavailable now` | DeepSeek 目前没有这一档 |

`json_schema` 严格模式是 OpenAI 的能力，DeepSeek 还没有。

**这个差别决定了今天的重点**：没有服务端强约束，就只能靠「prompt 规定 + 本地校验」两件一起做。少一件都不行。

---

## 二、四站实测结果

同一条客户消息：`我上周买的杯子裂了，订单号 SF1234567，我要退款，明天之前必须给答复。`
五样信息原文里全都有，所以只要字段对、内容对，就该是满分答案。

| 站 | 加了什么 | 直接能解析 | 字段名对 | 结论 |
|---|---|---|---|---|
| 1 | 只说「用 JSON 输出」 | ✓ | ✗（`订单号` / `问题类型` / `紧急程度`…） | 能解析，不能直接用 |
| 2 | + `json_object` | ✓ | ✗（同上，还是中文名） | 合法，但不合你的约 |
| 3 | + 字段名/类型/枚举写进 prompt | ✓ | ✓ | 能用 |
| 4 | 把第 2 站输出拿去校验 → 报错喂回 | — | 第 2 次通过 | 程序能自己修 |

第 3 站的实际输出：

```json
{"order_id": "SF1234567", "issue_type": "质量", "refund_requested": true,
 "urgency": 5, "key_phrases": ["杯子裂了", "我要退款", "明天之前必须给答复"]}
```

---

## 三、为什么「合法 JSON」远远不够

第 1、2 站交出来的东西，`json.loads` 一次就过，你看一眼也不觉得有错。但你的代码里写的是：

```python
order_id = data["order_id"]      # 它给的是 data["订单号"]
```

**当场 KeyError。** 而且这个错很阴：JSON 是合法的、内容是准确的、你肉眼检查两遍都挑不出毛病，只有跑起来才炸。

一句话：**`json_object` 保证的是「语法」，不是「你的接口」。** 语法是它的自由，字段名是你的规定——你规定，它遵守；你不规定，它自己起。

---

## 四、把「你要的形状」写成代码：Pydantic

prompt 里规定字段名，管住了 95% 的情况；剩下那 5% 靠代码兜底。写法就是把形状写成一个类：

```python
from typing import Literal
from pydantic import BaseModel, Field

class Ticket(BaseModel):
    order_id: str | None                                  # 可以没有，但不能是别的类型
    issue_type: Literal["物流", "质量", "退款", "其他"]     # 枚举，其它值直接判错
    refund_requested: bool
    urgency: int = Field(ge=1, le=5)                       # 范围
    key_phrases: list[str] = Field(min_length=1, max_length=3)   # 条数
```

然后一行校验：

```python
ticket = Ticket.model_validate(data)     # 不合格就抛 ValidationError，合格就给你一个对象
```

好处有三个，按重要性排：

1. **判据唯一**。什么叫"合格"写在类里，不在你的脑子里，也不在某个人的口头约定里。
2. **报错具体**。`字段 order_id：Field required`，直接指到是哪个字段、错在哪。
3. **后面全都有类型提示**。`ticket.urgency` 是 `int`，编辑器能补全，写错类型当场标红。

---

## 五、形状对 ≠ 内容对（今天最值钱的一条）

第 3 站五道校验全过：字段齐、类型对、枚举合法、范围合法。**但它仍然可能在编内容。**

比如它给你 `key_phrases: ["客户要求全额退款并赔偿"]` —— 形状完美，原文里根本没这句。**Pydantic 管不了这件事，因为「这句话必须出现在原文里」不是形状，是业务规则。**

所以脚本里还有第二层：

```python
def check_content(data):
    bad = [p for p in data.key_phrases if p not in MSG]   # 逐条回原文里找
    return bad
```

两层分工记清楚：

| 层 | 管什么 | 用什么写 |
|---|---|---|
| 形状层 | 字段名、类型、枚举、范围、必填 | Pydantic / JSON Schema |
| 业务层 | 单号是否真存在、原话是否逐字来自原文、金额是否等于订单金额 | **你自己的代码，没有现成工具** |

Day18 那个「编出来的订单号」问题，真正的解药在这里：**不是把 prompt 写得更狠，是代码里去查一次。** prompt 是劝告，校验是执法。

---

## 六、校验不过怎么办：把报错喂回去

第 4 站做的就是这个。第一次校验失败，报错是：

```
- 字段 order_id：Field required
- 字段 issue_type：Field required
- 字段 refund_requested：Field required
- 字段 urgency：Field required
- 字段 key_phrases：Field required
```

把这五行原文塞进对话，让模型自己改：

```python
messages = [
    {"role": "system",    "content": SCHEMA_PROMPT},
    {"role": "user",      "content": MSG},
    {"role": "assistant", "content": 上次的错误输出},      # 让它看见自己错在哪
    {"role": "user",      "content": "校验器报错如下：\n" + 报错原文 + "\n请重新输出。"},
]
```

实测第 2 次就通过了。这个模式叫**修复循环**（repair loop），是所有生产级结构化输出的标配。

三条纪律：

1. **必须设上限**。脚本写的 3 次。三次不过说明是 prompt 或模型的问题，再试只是烧钱。
2. **报错要原文转述**，不要自己总结成「格式不对」。模型的修改能力和报错的精确度成正比。
3. **重试要计成本**。脚本最后那行 `本次共消耗 936 tokens（含重试）` 就是给你看的——一次失败重试，成本直接翻倍。

---

## 七、跟 Day12 的 Function Calling 是什么关系

同一件事的两种入口：

| | 怎么用 | 适合 |
|---|---|---|
| `response_format=json_object` | 让它交一段 JSON 给你 | 你要的是**数据**（抽字段、分类、打分） |
| `tools` + `function` 的 JSON Schema | 让它选一个函数、填好参数 | 你要的是**动作**（查天气、发邮件、写数据库） |

两者都用 schema 约束，都不可信，都要本地校验。区别只是你拿到之后是"存起来"还是"执行它"。

---

## 八、什么时候用

| 场景 | 做法 |
|---|---|
| 一次性探索、人眼看结果 | 什么都别加，让它随便说 |
| 结果要进数据库 / 进下游程序 | `json_object` + 字段名写死 + Pydantic 校验 |
| 结果会被自动执行（下单、转账、发消息） | 上面全部，再加业务核对 + 人工确认 |
| 字段偶尔飘 | 加修复循环（报错喂回，最多 3 次） |

口诀：**先用 prompt 规定形状，再用代码确认形状，最后用业务确认内容。**

---

## 九、今天的一句话

> **能解析不等于能用，能用不等于对。**
> 形状交给 schema，真假交给代码，别指望一句 prompt 两头都管。
