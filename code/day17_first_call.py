"""Day17：第一次真正调用一个模型。

跑法：
    .venv\\Scripts\\python.exe -X utf8 code\\day17_first_call.py

前提：在仓库根目录放一个 .env，里面一行
    DEEPSEEK_API_KEY=sk-你的钥匙
（.env 已经在 .gitignore 里，不会被提交）

三段：
  1. 一次最普通的对话 —— 把回执的原始 JSON 和三个关键字段摆出来
  2. 让模型给一条评论打 1~5 分，温度设 0
  3. 一模一样再打一次 —— 看温度 0 是不是真的能复现

注意：脚本不会把钥匙打印出来，也不会写进任何文件。
"""

import json
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"


def load_key():
    """从仓库根目录的 .env 里读出钥匙；读不到就返回 None。"""
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if not env_file.exists():
        return None
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("DEEPSEEK_API_KEY="):
            return line.split("=", 1)[1].strip()
    return None


def ask(key, messages, temperature=1.0):
    """寄一个包裹出去，把回执解析成 Python 字典拿回来。"""
    body = {"model": MODEL, "messages": messages, "temperature": temperature}
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",      # 钥匙放头部，绝不写死在代码里
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def explain_error(code, text):
    """把状态码翻译成人话。"""
    hints = {
        401: "钥匙不对或没带 —— 检查 .env 里那串是不是完整复制了，有没有多余空格",
        402: "余额不足 —— 去开放平台充值，充最小额度就够练",
        429: "请求太快 —— 等一下再跑",
        500: "对面服务器出问题 —— 不是你代码的问题，过一会儿再试",
    }
    print(f"  HTTP {code}：{hints.get(code, '没见过的错误')}")
    print(f"  对方返回：{text[:300]}")


key = load_key()
if not key:
    print("没找到钥匙。按这个顺序办：")
    print("  1. 浏览器打开 https://platform.deepseek.com  注册并登录")
    print("  2. 左侧「API keys」-> 「创建 API key」-> 复制那串 sk- 开头的")
    print("  3. 在仓库根目录新建文件 .env，写一行：")
    print("       DEEPSEEK_API_KEY=sk-你复制的那串")
    print("  4. 左边「充值」充最小额度（几块钱能跑很多次）")
    print("  5. 再跑一遍这个脚本")
    raise SystemExit(0)

print("=" * 60)
print("第一段：一次最普通的对话")
print("=" * 60)

try:
    reply = ask(
        key,
        [{"role": "user", "content": "用一句话解释什么是 token，不超过 30 个字。"}],
        temperature=0,
    )
except urllib.error.HTTPError as e:
    explain_error(e.code, e.read().decode("utf-8", "ignore"))
    raise SystemExit(1)

print()
print("--- 原始回执（就是一段 JSON）---")
print(json.dumps(reply, ensure_ascii=False, indent=2))
print()
print("--- 你真正要看的三个字段 ---")
choice = reply["choices"][0]
print(f"  choices[0].message.content = {choice['message']['content']!r}")
print(f"  choices[0].finish_reason   = {choice['finish_reason']!r}")
print(f"  usage                      = {reply['usage']}")
print()

print("=" * 60)
print("第二段：让模型打分，温度设 0")
print("=" * 60)

comment = "物流很快，但是箱子被压扁了，里面的杯子裂了一道缝。"
task = [
    {
        "role": "system",
        "content": "你是客服质检员。只输出一个 1~5 的整数，不要任何解释。",
    },
    {"role": "user", "content": comment},
]

score1 = ask(key, task, temperature=0)["choices"][0]["message"]["content"]
print(f"  第一次打分：{score1.strip()}")

print()
print("=" * 60)
print("第三段：一模一样再打一次")
print("=" * 60)

score2 = ask(key, task, temperature=0)["choices"][0]["message"]["content"]
print(f"  第二次打分：{score2.strip()}")
print()
same = score1.strip() == score2.strip()
print(f"  两次是否完全一致：{same}")
print()
print("  温度 0 = 不抽签、每次取概率最高的那个 —— 这就是 Day15 那道")
print("  「200 条评论跑两遍分数不一样」的答案：默认温度不是 0，它每次都重新抽签。")
