# Day6 · 文件、JSON、路径

> 一句话：**程序活不过一次关机，除非它把状态写进文件。**
> Agent 也一样 —— 对话历史、工具返回、任务进度，全靠 JSON 存下来。

---

## 一、读写文件：三行就够

```python
from pathlib import Path

p = Path("todo.json")
text = p.read_text(encoding="utf-8")        # 读：整个文件变一个字符串
p.write_text("hello", encoding="utf-8")     # 写：整个字符串覆盖进文件
p.exists()                                  # 文件在不在
```

**`encoding="utf-8"` 必须写。** Windows 默认是 GBK，不写的话：读含中文的文件会
`UnicodeDecodeError`，写出来的文件在别的程序里是乱码。这一条能省你两小时。

**`open()` 和 `Path` 的关系**：`Path.read_text()` 就是 `with open(...) as f: f.read()` 的简写，
不用自己 `close()`。初学阶段直接用 `Path` 的写法，忘记 `close` 的坑就绕过去了。

---

## 二、JSON：字符串 <-> Python 对象

| 方向 | 函数 | 记法 |
|---|---|---|
| 字符串 → Python | `json.loads(text)` | **l**oad**s** = load **s**tring |
| Python → 字符串 | `json.dumps(obj)` | **d**ump**s** = dump **s**tring |
| 文件 → Python | `json.load(f)` | 没有 s，直接吃文件对象 |
| Python → 文件 | `json.dump(obj, f)` | 没有 s |

**你只需要记住 `loads` / `dumps` 这一对**，文件那两个等价于「先读成字符串再 loads」。

### 类型对照（JSON 只有这几种）

| Python | JSON |
|---|---|
| `dict` | object `{}` |
| `list` | array `[]` |
| `str` | string `""` |
| `int` / `float` | number |
| `True` / `False` | `true` / `false` |
| `None` | `null` |
| `tuple` / `set` / `datetime` | **没有对应类型**，会报错或变成 list/str |

### 两个必设参数

```python
json.dumps(data, ensure_ascii=False, indent=2)
```

- `ensure_ascii=False` → 中文存成 `"读完字典"` 而不是 `"\u8bfb\u5b8c\u5b57\u5178"`（不加也能用，但人看不懂）
- `indent=2` → 缩进两格，人能读。程序不在乎，你在乎。

---

## 三、路径：为什么用 `Path(__file__).parent`

```python
DATA_FILE = Path(__file__).parent / "todo.json"
```

- `__file__` = 这个脚本自己的路径
- `.parent` = 它所在的目录
- 所以数据文件**永远在脚本旁边**，跟你在哪个目录敲命令无关

如果用 `Path("todo.json")`（相对路径），你在 `C:\Users\22155` 敲命令，文件就建在那里；
在仓库里敲，就建在仓库里 —— 同一个程序，数据跑到两个地方，这是新手最常见的"数据丢了"。

> 这就是 Day4 那次 `code\day04_guess.py` 打开成空白文件的同一个原理：相对路径跟着「当前目录」走。

---

## 四、安全写法：先写临时文件，再替换

```python
tmp = DATA_FILE.parent / (DATA_FILE.name + ".tmp")
tmp.write_text(json.dumps(todos, ensure_ascii=False, indent=2), encoding="utf-8")
tmp.replace(DATA_FILE)      # 原子替换
```

直接覆盖原文件，如果写到一半断电 / 程序崩，`todo.json` 就变成半截乱码，数据全没。
先写 `.tmp` 再替换，最坏情况也只是 `.tmp` 坏了，原文件完好。数据库、配置文件都是这么干的。

---

## 五、异常处理：三种坏情况都要接住

| 情况 | 会抛什么 | 怎么处理 |
|---|---|---|
| 文件不存在 | 不抛，`exists()` 判断 | 返回空清单 |
| 文件存在但没权限 | `OSError` / `PermissionError` | 提示用户，不要崩 |
| 文件里不是合法 JSON | `json.JSONDecodeError` | 当空清单，或提示"文件坏了" |

`day06_todo.py` 的 `load_todos()` 就是这三层的模板 —— 一个"读配置文件"的函数，
以后写任何项目都可以照抄这个骨架。

---

## 六、Agent 视角：为什么今天这课是刚需

| Agent 里的东西 | 存在哪 |
|---|---|
| 对话历史 messages | JSON 数组 |
| 工具调用 tool_calls | JSON 对象 |
| 任务中间状态（做到第几步） | JSON 文件 |
| 配置（模型名、温度、API 地址） | JSON / YAML |
| 向量库里的元数据 | JSON |

大模型的 API **请求体和返回体都是 JSON**。你和小模型说话、模型和工具说话、工具和你说回来，
全程都是 `json.dumps` → 网络 → `json.loads`。今天不熟，Day40 写 Function Calling 时会寸步难行。

---

## 七、今天只求记住四行

```python
text = Path("todo.json").read_text(encoding="utf-8")
data = json.loads(text)
text = json.dumps(data, ensure_ascii=False, indent=2)
Path("todo.json").write_text(text, encoding="utf-8")
```

读、转、转回、写。就这四步。

---

## 八、改一处（10 分钟，任选一个）

1. `add` 时顺便记时间：加 `"created": datetime.now().isoformat()` —— 会遇到
   `datetime` 不是 JSON 类型的报错，体验一次「类型不对」，用 `.isoformat()` 转成字符串解决
2. `list` 时只显示未完成的：`if not t["done"]`
3. 加一个 `undone` 命令，把 `[x]` 改回 `[ ]`
4. 故意把 `todo.json` 手动改坏（删掉一个引号），再跑 `list` —— 看它怎么兜底

---

## 九、我踩的坑

（自己填，写真实遇到的，一两行就够）

## 十、一句话总结

（自己写，比如「程序的状态要落盘，落盘用 JSON，JSON 的两个函数是 loads 和 dumps」）
