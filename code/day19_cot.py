"""Day19：思维链与系统提示 —— 修好 Day18 那个漏抽

跑法：
    .venv\\Scripts\\python.exe -X utf8 code\\day19_cot.py

Day18 留了个问题：V4 写了「没有明确写出的就填 null」，结果
「不给退我就去投诉」这句被判成 null —— 防住了编造，却漏掉了该抽的。

今天试四种写法，看哪种真的两边都站住：
  A 严格 + 示例   —— Day18 的 V4 原样（全字段都要求「明确写出」，用户消息里带一条示例）
  B 严格 + 无示例 —— 规则不动，只把那条示例拿掉
  C 放宽 + 示例   —— 规则改成「能合理推断就填」
  D 分字段 + 依据 —— order_id 死守原文，refund 按诉求判断，并先输出一行依据

最后还有一段 2×2 补测：严格/放宽 × 带/不带示例，用来验证「到底是示例教坏了它，
还是示例放大了规则的严格程度」。实测只有「严格 + 示例」一格失败。

两个指标是反向的，必须同时满足才算对：
  order_id         必须是 null（原文没有单号，编了就是错）
  refund_requested 必须是 true（「不给退我就去投诉」是明确诉求）
"""

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

MSG = "我上周买的那个杯子裂了，订单号好像是 SF 开头的一串，你们看着办吧，不给退我就去投诉。"


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
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


BASE = (
    "你是客服工单助手。规则：\n"
    "1. 只输出一个 JSON 对象。不要用 markdown 代码块包裹，不要任何解释。\n"
    "2. 三个字段必须都有：order_id 字符串、issue_type 枚举、refund_requested 布尔值。\n"
    "3. issue_type 只能是：物流 / 质量 / 退款 / 其他。\n"
)

SHOT = (
    "消息：「订单 A12345 的快递三天没动，我要退款」\n"
    '输出：{"order_id": "A12345", "issue_type": "物流", "refund_requested": true}\n\n'
    "消息：\n" + MSG
)

FIELDS_RULE = (
    "你是客服工单助手。按两步输出：\n"
    "第一步，输出一行「依据：<一句话，说明你是从原文哪句话得出的结论>」；\n"
    "第二步，输出 JSON。各字段规则不同，必须分别遵守：\n"
    "- order_id：必须能在原文里找到完整的单号原文；找不到就填 null，"
    "绝不允许自己补全或编造。\n"
    "- issue_type：只能是 物流 / 质量 / 退款 / 其他。\n"
    "- refund_requested：客户明确提出「要退 / 要退钱 / 要退款 / 要退货」"
    "这类诉求就填 true；只抱怨、威胁投诉、追问进度但没提退款的填 false；"
    "完全没涉及退款才填 null。\n"
    "JSON 只输出一个对象，不要用 markdown 代码块包裹。"
)

# 每条：(说明, system, user, 有没有示例)
VERSIONS = [
    ("A 严格+示例", BASE + "4. 消息里没有明确写出的信息一律填 null，绝对不要猜、不要编。",
     SHOT, "有（Day18 原样）"),

    ("B 严格+无示例", BASE + "4. 消息里没有明确写出的信息一律填 null，绝对不要猜、不要编。",
     MSG, "无"),

    ("C 放宽+示例", BASE + "4. 信息没有明确写出时，可以根据上下文合理推断；"
                           "完全推断不出来才填 null。",
     SHOT, "有"),

    ("D 分字段+依据", FIELDS_RULE, SHOT, "有"),
]


def extract_json(text):
    """从「依据 + JSON」这种混合输出里，只取最后一个完整的 {...}。"""
    i = text.find("{")
    j = text.rfind("}")
    if i == -1 or j <= i:
        return None
    try:
        return json.loads(text[i:j + 1])
    except Exception:
        return None


def judge(data):
    """两个反向指标，同时对才算过。"""
    if data is None:
        return "✗", "解析失败", "✗", "✗"
    oid = data.get("order_id")
    refund = data.get("refund_requested")
    oid_ok = "✓" if oid is None else "✗"
    oid_show = "null" if oid is None else f"编了 {oid}"
    if refund is True:
        refund_ok, refund_show = "✓", "true"
    elif refund is False:
        refund_ok, refund_show = "✗", "false（判反了）"
    else:
        refund_ok, refund_show = "✗", "null（漏抽）"
    all_ok = "✓" if (oid_ok == "✓" and refund_ok == "✓") else "✗"
    return oid_ok, oid_show, refund_ok + " " + refund_show, all_ok


key = load_key()
if not key:
    print("没找到钥匙，先按 Day17 把 .env 填好。")
    raise SystemExit(0)

print("=" * 68)
print("同一条消息、温度 0，只改约束写法 —— 看能不能既「不编」又「不漏」")
print("=" * 68)
print(f"\n消息：{MSG}\n")
print("正确答案：order_id = null（原文没给单号）；refund_requested = true（要退款）\n")

rows = []
for name, system, user, has_shot in VERSIONS:
    reply = ask(key, [{"role": "system", "content": system},
                      {"role": "user", "content": user}])
    text = reply["choices"][0]["message"]["content"]
    data = extract_json(text)
    rows.append((name, has_shot, text, judge(data)))

    print("-" * 68)
    print(f"【{name}】 示例：{has_shot}")
    print("-" * 68)
    shown = text if len(text) <= 300 else text[:300] + " …"
    print(shown.strip())
    print()

print("=" * 68)
print("结果对照")
print("=" * 68)
print()
print(f"{'版本':<14}{'order_id':<20}{'refund_requested':<24}{'两边都对'}")
print("-" * 68)
for name, has_shot, text, (oid_ok, oid_show, refund_show, all_ok) in rows:
    print(f"{name:<14}{oid_ok + ' ' + oid_show:<20}{refund_show:<24}{all_ok}")
print()
print()
print("=" * 68)
print("补测：2×2 —— 示例真的是在「教标准」吗？")
print("=" * 68)
print()

STRICT = BASE + "4. 消息里没有明确写出的信息一律填 null，绝对不要猜、不要编。"
LOOSE = BASE + "4. 信息没有明确写出时，可以根据上下文合理推断；完全推断不出来才填 null。"

grid = {}
for rname, rsys in (("严格规则", STRICT), ("放宽规则", LOOSE)):
    for ename, euser in (("不带示例", MSG), ("带示例", SHOT)):
        reply = ask(key, [{"role": "system", "content": rsys},
                          {"role": "user", "content": euser}])
        data = extract_json(reply["choices"][0]["message"]["content"])
        val = "解析失败" if data is None else str(data.get("refund_requested"))
        grid[(rname, ename)] = val

print(f"{'':<10}{'不带示例':<14}{'带示例'}")
print("-" * 44)
for rname in ("严格规则", "放宽规则"):
    a = grid[(rname, "不带示例")]
    b = grid[(rname, "带示例")]
    print(f"{rname:<10}{a:<14}{b}")
print()
print("四格只坏一格：严格规则 + 示例 —— 各自单独都好好的。")
print()

print("=" * 68)
print("该看出来的四件事")
print("=" * 68)
print("1. 先看 A 和 B：规则一字不差，只差 user 里那条示例在不在，结果就从 null")
print("   变成 true。第一反应一定是「示例把它教窄了」—— 但先别急着下结论。")
print("2. 上面那个 2×2 就是为了验证这句话。结论是它只对一半：放宽规则下带不带示例")
print("   都是 true，坏的只有「严格规则 + 示例」这一格。")
print("   机制：规则写了「没明说就 null」，等于留了一个随时能退的出口；示例又给了")
print("   一个「合格答案长什么样」的实物。两者一凑，判据就从「有没有这个诉求」")
print("   换成了「像不像这一条」。规则不放宽，那个出口不在，示例再规整也无处可退。")
print("   —— 一句话：**示例不改规则，只放大规则。**")
print("3. C 放宽这次也对上了，没测到它编造单号 —— 所以不能说它一定错。它的毛病")
print("   是边界模糊：「合理推断」到哪算合理，你说了不算，也拿不出依据复核。")
print("4. D 把松紧拆到字段上（单号死守原文、退款按诉求判），并要求先写一行依据。")
print("   多出来的那行「依据」不是装饰：它让每个结论都能被人核对，也让模型")
print("   先想后答。代价是输出变成两段，代码只能抓最后那个 JSON 块。")

