"""Day18：Prompt 四件套对照实验（角色 / 任务 / 约束 / 格式）

跑法：
    .venv\\Scripts\\python.exe -X utf8 code\\day18_prompt_ab.py

同一个任务、同一条消息、温度全设 0，只改提示词写法，比较四版输出的差别。
四版是递进的：
  V1 裸问        —— 什么都不说，只把消息丢过去
  V2 只给任务    —— 说要抽哪三个字段，但不说格式
  V3 加输出格式  —— 给 JSON 骨架 + 枚举值
  V4 加约束      —— 再加「不许编、没有就 null」+ 一条示例

脚本最后自动检查四件事，不靠感觉：
  1. 能不能直接 json.loads（还是被 ```json 围栏包住）
  2. 三个字段齐不齐
  3. issue_type 在不在允许的枚举里
  4. 消息里根本没给的订单号，它有没有编一个出来

注意：这条消息故意没写订单号（只说「好像是 SF 开头的一串」），
      编不编，就是这堂课的核心。
"""

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"


def load_key():
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if not env_file.exists():
        return None
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("DEEPSEEK_API_KEY="):
            return line.split("=", 1)[1].strip()
    return None


def ask(key, messages, temperature=0):
    body = {"model": MODEL, "messages": messages, "temperature": temperature}
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


# 故意含糊：没有真订单号，只有「好像是 SF 开头的一串」
MSG = "我上周买的那个杯子裂了，订单号好像是 SF 开头的一串，你们看着办吧，不给退我就去投诉。"

ALLOWED = {"物流", "质量", "退款", "其他"}
REQUIRED = {"order_id", "issue_type", "refund_requested"}

versions = []

# ---------- V1：裸问 ----------
versions.append((
    "V1 裸问",
    [{"role": "user", "content": f"这条客服消息说了什么？\n\n{MSG}"}],
))

# ---------- V2：只给任务 ----------
versions.append((
    "V2 只给任务",
    [{"role": "user", "content":
      f"从下面这条客服消息里抽出：订单号、问题类型、是否要求退款。\n\n{MSG}"}],
))

# ---------- V3：加输出格式 ----------
versions.append((
    "V3 加输出格式",
    [
        {"role": "system", "content": "你是客服工单助手。"},
        {"role": "user", "content":
            "从下面这条客服消息里抽取字段，输出 JSON：\n"
            '{"order_id": ..., "issue_type": ..., "refund_requested": ...}\n'
            "issue_type 只能是：物流 / 质量 / 退款 / 其他\n\n"
            f"消息：\n{MSG}"},
    ],
))

# ---------- V4：再加约束 + 示例 ----------
versions.append((
    "V4 加约束 + 示例",
    [
        {"role": "system", "content":
            "你是客服工单助手。规则：\n"
            "1. 只输出一个 JSON 对象。不要用 markdown 代码块包裹，不要任何解释。\n"
            "2. 三个字段必须都有：order_id 字符串、issue_type 枚举、refund_requested 布尔值。\n"
            "3. issue_type 只能是：物流 / 质量 / 退款 / 其他。\n"
            "4. 消息里没有明确写出的信息一律填 null，绝对不要猜、不要编。"},
        {"role": "user", "content":
            '消息：「订单 A12345 的快递三天没动，我要退款」\n'
            '输出：{"order_id": "A12345", "issue_type": "物流", "refund_requested": true}\n\n'
            f"消息：\n{MSG}"},
    ],
))


def inspect(text):
    """返回 5 个硬指标 + 一句备注。"""
    raw = text.strip()
    fenced = raw.startswith("```")
    if fenced:
        raw = re.sub(r"^```[a-zA-Z]*\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw).strip()
    try:
        data = json.loads(raw)
    except Exception as exc:
        return {"直接解析": "✗", "字段齐全": "-", "枚举合法": "-", "布尔值": "-",
                "order_id": "-", "备注": f"{type(exc).__name__}（不是纯 JSON）"}

    fields_ok = REQUIRED <= set(data.keys())
    enum_ok = data.get("issue_type") in ALLOWED
    bool_ok = isinstance(data.get("refund_requested"), bool)
    oid = data.get("order_id")
    if oid is None:
        oid_tag = "null"
    else:
        oid_tag = f"填了：{oid}"
    note = "剥掉 ``` 围栏才解析成功" if fenced else "纯 JSON，可直接解析"
    return {
        "直接解析": "△" if fenced else "✓",
        "字段齐全": "✓" if fields_ok else "✗",
        "枚举合法": "✓" if enum_ok else "✗",
        "布尔值": "✓" if bool_ok else "✗",
        "order_id": oid_tag,
        "备注": note,
    }


key = load_key()
if not key:
    print("没找到钥匙，先把 .env 里的 DEEPSEEK_API_KEY 填好（见 Day17）。")
    raise SystemExit(0)

print("=" * 66)
print("同一个任务、同一条消息、温度 0 —— 只改提示词，看输出怎么变")
print("=" * 66)
print(f"\n消息原文：{MSG}\n")
print("这条消息里根本没有订单号（只说「好像是 SF 开头的一串」）——")
print("所以正确的 order_id 只能是 null。它要是给了个具体的号，就是编的。\n")

results = []
for name, messages in versions:
    reply = ask(key, messages)
    text = reply["choices"][0]["message"]["content"]
    used = reply["usage"]["total_tokens"]
    results.append((name, text, used, inspect(text)))

    print("-" * 66)
    print(f"【{name}】  tokens={used}")
    print("-" * 66)
    shown = text if len(text) <= 420 else text[:420] + " …(截断)"
    print(shown.strip())
    print()

print("=" * 66)
print("自动检查（不靠感觉，靠代码判断）")
print("=" * 66)
print()
print(f"{'版本':<16}{'直接解析':<10}{'字段齐全':<10}{'枚举合法':<10}{'布尔值':<8}{'order_id'}")
print("-" * 66)
for name, text, used, r in results:
    print(f"{name:<16}{r['直接解析']:<10}{r['字段齐全']:<10}{r['枚举合法']:<10}{r['布尔值']:<8}{r['order_id']}")
print()
print("备注：")
for name, text, used, r in results:
    print(f"  {name}：{r['备注']}")
print()
print("=" * 66)
print("该看出来的三件事")
print("=" * 66)
print("1. V1 交的是散文，V3/V4 交的是 JSON。差别不在模型聪明不聪明，在于")
print("   你有没有说清「交什么格式」。字段名不指定，它每次给你起的名字都不一样。")
print("2. 那句 system 里写「你是客服工单助手」，只定了身份，没定格式，所以 V3")
print("   之前的两版照样给你人话。角色是最弱的一条，格式才是最硬的一条。")
print("3. 重点看 V3 和 V4 的布尔值那一列：V3 判 true（「不给退我就去投诉」），")
print("   V4 判 null（因为规则说「没明确写出的填 null」，模型认定这句是暗示）。")
print("   —— 约束能防编造，但写太死会把该抽的也漏掉。这一条留到 Day19 细讲。")

