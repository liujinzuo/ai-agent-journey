"""Day6 · 命令行 Todo —— 数据存在 todo.json，关掉再开还在。

用法（在 PowerShell 里，仓库根目录下）：
    python code/day06_todo.py list
    python code/day06_todo.py add "读完 5.5 字典"
    python code/day06_todo.py done 1
    python code/day06_todo.py rm 1
    python code/day06_todo.py clear

今天要看的四件事：
    1. Path(__file__).parent  —— 让数据文件永远跟着脚本走，跟你在哪个目录敲命令无关
    2. read_text / write_text(encoding="utf-8")  —— 不写 encoding，中文在 Windows 上会乱码
    3. json.loads / json.dumps  —— 字符串 <-> Python 对象（list / dict）
    4. 存临时文件再 replace  —— 写到一半断电，也不会把原文件写坏
"""

import json
import sys
from pathlib import Path

# 数据文件放在脚本旁边，而不是"当前工作目录"
DATA_FILE = Path(__file__).parent / "todo.json"


# ---------- 存取 ----------

def load_todos():
    """读 todo.json，返回 list。文件不存在 / 内容坏了都不崩。"""
    if not DATA_FILE.exists():
        return []
    try:
        text = DATA_FILE.read_text(encoding="utf-8")
    except OSError as e:
        print(f"[警告] 读不了 {DATA_FILE.name}：{e}")
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        print(f"[警告] {DATA_FILE.name} 不是合法 JSON，本次按空清单处理")
        return []
    if not isinstance(data, list):
        return []
    return data


def save_todos(todos):
    """先写临时文件，成功后再替换，避免写一半把原数据弄坏。"""
    tmp = DATA_FILE.parent / (DATA_FILE.name + ".tmp")
    tmp.write_text(
        json.dumps(todos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    tmp.replace(DATA_FILE)


# ---------- 业务 ----------

def next_id(todos):
    return max([t["id"] for t in todos], default=0) + 1


def cmd_add(todos, text):
    if not text:
        print("用法：python code/day06_todo.py add \"要做的事\"")
        return
    todos.append({"id": next_id(todos), "text": text, "done": False})
    save_todos(todos)
    print(f"已添加：{text}")


def cmd_list(todos):
    if not todos:
        print("清单是空的。用 add 加一条试试。")
        return
    for t in todos:
        mark = "[x]" if t["done"] else "[ ]"
        print(f'{t["id"]:>3}. {mark} {t["text"]}')
    left = sum(1 for t in todos if not t["done"])
    print(f"\n共 {len(todos)} 条，未完成 {left} 条。数据文件：{DATA_FILE.name}")


def cmd_done(todos, raw_id):
    tid = to_id(raw_id)
    for t in todos:
        if t["id"] == tid:
            t["done"] = True
            save_todos(todos)
            print(f"已完成：{t['text']}")
            return
    print(f"没有 id = {tid} 的条目（先 list 看一眼）")


def cmd_rm(todos, raw_id):
    tid = to_id(raw_id)
    kept = [t for t in todos if t["id"] != tid]
    if len(kept) == len(todos):
        print(f"没有 id = {tid} 的条目（先 list 看一眼）")
        return
    save_todos(kept)
    print(f"已删除 id = {tid}")


def cmd_clear(todos):
    save_todos([])
    print("清单已清空")


def to_id(raw):
    """把命令行传来的字符串转成 int，转不了就返回 -1（永远对不上任何条目）。"""
    try:
        return int(raw)
    except (TypeError, ValueError):
        print(f"id 必须是数字，你给的是 {raw!r}")
        return -1


# ---------- 入口 ----------

def main(argv):
    todos = load_todos()
    command = argv[1] if len(argv) > 1 else "list"
    arg = " ".join(argv[2:]) if len(argv) > 2 else ""

    if command == "add":
        cmd_add(todos, arg)
    elif command == "list":
        cmd_list(todos)
    elif command == "done":
        cmd_done(todos, arg)
    elif command == "rm":
        cmd_rm(todos, arg)
    elif command == "clear":
        cmd_clear(todos)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv)
