"""Day13 演示：你的程序是怎么"问"模型的。

跑法：
    .venv\\Scripts\\python.exe -X utf8 code\\day13_fake_llm.py

脚本里起了一个假的"模型服务器"（就在本机，不需要联网、不需要 API key），
然后用两次真实的 HTTP 请求去敲它：一次不带钥匙，一次带钥匙。
目的是让你亲眼看到"请求"这东西长什么样、钥匙到底管什么用。
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

# 服务器认可的钥匙。真实世界里这是你在平台上申请的那串 sk-xxxx
GOOD_KEY = "sk-test-123"

# 服务器收到请求后要回的那段内容（模仿真实模型的回复格式）
MODEL_REPLY = {
    "role": "assistant",
    "content": "",
    "tool_calls": [{"name": "get_weather", "arguments": {"city": "北京", "days": 3}}],
}


class FakeModel(BaseHTTPRequestHandler):
    """假的模型服务器：只认一条路 /v1/chat，只认一把钥匙。"""

    def do_POST(self):
        # 1. 先查钥匙
        auth = self.headers.get("Authorization", "")
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8")

        print("  [服务器] 收到请求：", self.path)
        print("  [服务器] 看到钥匙：", auth if auth else "(空的)")
        print("  [服务器] 收到内容：", raw_body)

        if auth != f"Bearer {GOOD_KEY}":
            self._send(401, {"error": "钥匙不对或没带钥匙"})
            return

        # 2. 钥匙对了，把请求内容解析出来，回一段"模型的回答"
        body = json.loads(raw_body)
        print("  [服务器] 用户问了：", body["messages"][-1]["content"])
        self._send(200, MODEL_REPLY)

    def _send(self, code, payload):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass  # 关掉服务器自带的流水日志，免得刷屏


def ask_model(url, api_key=None):
    """向模型发一次请求。api_key 为 None 表示没带钥匙。"""
    payload = {
        "model": "fake-model",
        "messages": [{"role": "user", "content": "北京未来三天天气怎么样？"}],
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    print("=" * 52)
    print("寄出的包裹：")
    print("  地址：", url)
    print("  方法： POST")
    print("  钥匙：", headers.get("Authorization", "(没带)"))
    print("  内容：", json.dumps(payload, ensure_ascii=False))
    print("-" * 52)

    req = Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            print("收到回执：状态码", resp.status)
            print("回执内容：", body)
            return json.loads(body)
    except HTTPError as e:
        body = e.read().decode("utf-8")
        print("收到回执：状态码", e.code)
        print("回执内容：", body)
        return None


def main():
    server = HTTPServer(("127.0.0.1", 0), FakeModel)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/v1/chat"

    print("第一步：不带钥匙去敲门")
    ask_model(url)

    print()
    print("第二步：带上钥匙再敲一次")
    result = ask_model(url, api_key=GOOD_KEY)

    if result:
        call = result["tool_calls"][0]
        print()
        print("拿到模型的话之后，你的程序要做的事：")
        print(f"  它点了工具 {call['name']}，参数 {call['arguments']}")
        print("  —— 这就是 Day12 说的那张单子。")

    server.shutdown()


if __name__ == "__main__":
    main()
