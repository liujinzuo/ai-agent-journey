"""Day20：结构化输出 —— 让模型交出来的东西，代码能直接吃

跑法：
    .venv\\Scripts\\python.exe -X utf8 code\\day20_json_mode.py

Day18~19 你一直在用 extract_json 手工从一坨文字里抠 JSON。今天换思路：
不靠事后抠，靠事前约束。

四站，一档一档往上加：
  第 1 站  什么都不加，只在 prompt 里说「用 JSON」   —— 能不能解析？
  第 2 站  + response_format=json_object             —— 保证是合法 JSON
  第 3 站  + 把字段名和类型写进 prompt                —— 保证是「你要的那几个字段」
  第 4 站  校验不过就把报错原文喂回去重试              —— 让程序自己修

两件顺手验证的事：
  · DeepSeek 没有 json_schema 严格模式，所以本地校验必须自己写（Pydantic）
  · schema 只管形状，管不了内容真假 —— 所以还要一层业务核对
"""

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError
from typing import Literal

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

MSG = "我上周买的杯子裂了，订单号 SF1234567，我要退款，明天之前必须给答复。"

# 第 1、2 站用的 prompt：说了要什么信息，但没说字段名、没说类型
LOOSE_PROMPT = (
    "从客户消息里抽取这几样信息：订单号、问题类型（物流/质量/退款/其他）、"
    "客户是否要求退款、紧急程度（1~5）、几句关键原话。\n"
    "用 JSON 输出。"
)

# 第 3 站用的 prompt：字段名一字不差地规定死，类型、枚举、范围全部写明
SCHEMA_PROMPT = (
    "只输出一个 JSON 对象，不要 markdown 代码块包裹，不要任何解释。\n"
    "字段必须严格是下面五个，名字一字不差：\n"
    "- order_id: 字符串或 null。原文出现完整单号才填，否则 null，"
    "不许补全、不许编造。\n"
    "- issue_type: 字符串，只能是 \"物流\" / \"质量\" / \"退款\" / \"其他\" 之一。\n"
    "- refund_requested: 布尔值。明确要求退款填 true，否则 false。\n"
    "- urgency: 整数，1~5。1 最不急，5 最急。\n"
    "- key_phrases: 字符串数组，1~3 条，必须逐字摘自原文，不许改写。"
)

tokens_used = 0


def load_key():
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if not env_file.exists():
        return None
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("DEEPSEEK_API_KEY="):
            return line.strip().split("=", 1)[1].strip()
    return None


def ask(key, messages, response_format=None, temperature=0):
    global tokens_used
    body = {"model": MODEL, "messages": messages, "temperature": temperature}
    if response_format is not None:
        body["response_format"] = response_format
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    usage = data.get("usage") or {}
    tokens_used += (usage.get("prompt_tokens") or 0) + (usage.get("completion_tokens") or 0)
    return data["choices"][0]["message"]["content"]


def try_parse(text):
    """能不能直接 json.loads？返回 (数据 or None, 说明)。"""
    raw = text.strip()
    fenced = raw.startswith("```")
    if fenced:
        raw = re.sub(r"^```[a-zA-Z]*\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw).strip()
    try:
        return json.loads(raw), ("带 ``` 围栏，剥掉才解析成功" if fenced else "纯 JSON，直接解析成功")
    except Exception as exc:
        return None, f"{type(exc).__name__}：{exc}"


class Ticket(BaseModel):
    """这就是「你要的形状」。字段名、类型、枚举、范围，全在这里。"""

    order_id: str | None
    issue_type: Literal["物流", "质量", "退款", "其他"]
    refund_requested: bool
    urgency: int = Field(ge=1, le=5)
    key_phrases: list[str] = Field(min_length=1, max_length=3)


def check_shape(data):
    """形状对不对 —— 交给 Pydantic，不靠肉眼。"""
    try:
        return Ticket.model_validate(data), None
    except ValidationError as exc:
        return None, exc


def err_summary(exc):
    """把 Pydantic 的报错压成几行，既能给人看，也能喂回给模型。"""
    lines = []
    for item in exc.errors()[:6]:
        loc = ".".join(str(x) for x in item["loc"]) or "(根)"
        lines.append(f"- 字段 {loc}：{item['msg']}")
    return "\n".join(lines)


def check_content(data):
    """形状对了，不代表内容对。原话必须真在原文里 —— 这条 schema 管不了。"""
    bad = [p for p in data.key_phrases if p not in MSG]
    return bad


key = load_key()
if not key:
    print("没找到钥匙，先按 Day17 把 .env 填好。")
    raise SystemExit(0)

print("=" * 70)
print("客户消息：" + MSG)
print("=" * 70)
print()
print("注意：这条消息里五样信息全都有，而且单号是完整写出来的。")
print("所以下面任何一版，只要字段对、内容对，就应该是满分答案。")
print()

# ---------------------------------------------------------------- 第 1 站
print("-" * 70)
print("第 1 站：只在 prompt 里说「用 JSON 输出」，其他什么都不加")
print("-" * 70)
text1 = ask(key, [{"role": "system", "content": LOOSE_PROMPT},
                  {"role": "user", "content": MSG}])
data1, note1 = try_parse(text1)
print("它交的原文：")
print(text1.strip()[:400])
print()
print("解析结果：" + note1)
if data1:
    print("它自己起的字段名：" + " / ".join(data1.keys()))
print()

# ---------------------------------------------------------------- 第 2 站
print("-" * 70)
print("第 2 站：同一个 prompt，加上 response_format = json_object")
print("-" * 70)
text2 = ask(key, [{"role": "system", "content": LOOSE_PROMPT},
                  {"role": "user", "content": MSG}],
            response_format={"type": "json_object"})
data2, note2 = try_parse(text2)
print("它交的原文：")
print(text2.strip()[:400])
print()
print("解析结果：" + note2)
if data2:
    print("它自己起的字段名：" + " / ".join(data2.keys()))
print()
print("→ json_object 只保证「是合法 JSON」，不保证「是你要的字段」。")
print("  你的代码要 data[\"order_id\"]，它给你的是「订单号」—— KeyError 一样跑。")
print()

# ---------------------------------------------------------------- 第 3 站
print("-" * 70)
print("第 3 站：把字段名、类型、枚举、范围全写进 prompt，仍用 json_object")
print("-" * 70)
text3 = ask(key, [{"role": "system", "content": SCHEMA_PROMPT},
                  {"role": "user", "content": MSG}],
            response_format={"type": "json_object"})
data3, note3 = try_parse(text3)
print("它交的原文：")
print(text3.strip()[:400])
print()
print("解析结果：" + note3)
ticket, exc = check_shape(data3 if data3 else {})
if exc:
    print("形状校验 ✗：")
    print(err_summary(exc))
else:
    print("形状校验 ✓：五个字段全在、类型全对、枚举合法、urgency 在 1~5 内")
    bad = check_content(ticket)
    if bad:
        print(f"内容校验 ✗：这几条「原话」原文里根本没有 → {bad}")
    else:
        print("内容校验 ✓：key_phrases 每条都能在原文里逐字找到")
print()
print("→ 到这里才叫「能用」：形状对 + 内容对。少一样都是坑。")
print()

# ---------------------------------------------------------------- 第 4 站
print("-" * 70)
print("第 4 站：拿第 2 站那份「合法但字段不对」的输出，让程序自己修")
print("-" * 70)
if data2 is None:
    print("第 2 站没解析出来，这一步跳过。")
else:
    current = data2
    current_text = text2.strip()
    for attempt in range(1, 4):
        ticket, exc = check_shape(current)
        if exc is None:
            print(f"第 {attempt} 次校验：✓ 通过")
            break
        print(f"第 {attempt} 次校验：✗ 不通过")
        print(err_summary(exc))
        print()
        current_text = ask(key, [
            {"role": "system", "content": SCHEMA_PROMPT},
            {"role": "user", "content": MSG},
            {"role": "assistant", "content": current_text},
            {"role": "user", "content": "上面这个 JSON 不符合要求，校验器报错如下：\n"
                                        + err_summary(exc)
                                        + "\n请只重新输出一个符合要求的 JSON 对象，不要解释。"},
        ], response_format={"type": "json_object"})
        current, _ = try_parse(current_text)
        if current is None:
            print("    它这次交的东西连 JSON 都不是，重试中止。")
            break
        print("  已把报错原文喂回去，让它按报错改。")
        print()
    else:
        print("三次都没修好 —— 这种情况该换 prompt 或换模型，别再重试了。")

print()
print("=" * 70)
print(f"本次共消耗 {tokens_used} tokens（含重试）")
print("=" * 70)
print()
print("该记住的四件事")
print("-" * 70)
print("1. 「能解析」不等于「能用」。json_object 只保证格式合法，字段名它想怎么起")
print("   就怎么起。结构必须由你规定，不能指望它猜中。")
print("2. DeepSeek 没有 json_schema 严格模式（这一档要 OpenAI）。所以本地校验")
print("   不是可选项：Pydantic 定义一次，形状对错由代码判，不靠肉眼。")
print("3. 形状对也不等于内容对。schema 管不了「这句话原文里到底有没有」，")
print("   业务核对得自己写 —— 这就是 Day18 那个「编造单号」问题的真正解药。")
print("4. 校验失败别直接抛异常给用户。把报错原文喂回去让它改，通常一两次就过；")
print("   但重试必须有上限，三次不过就说明是 prompt 或模型的问题，别再烧钱。")
