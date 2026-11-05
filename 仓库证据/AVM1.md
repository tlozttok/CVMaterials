# AVM1 仓库证据

仓库：<https://github.com/tlozttok/AVM1>
本地：`D:\ComputerST\Code\Project\AVM1`（`git remote -v` 指向同一地址）

---

## 对应简历哪几句

| 简历行 | 句子 | 仓库里能证明的 |
|---|---|---|
| 22 | 删掉递归栈实现，重定接口与不变量，让 Agent 按新骨架重写 `[commit 9ad13c2]` | `9ad13c2` 的 diff：`avm/core.py` +268 / −685 |
| 22 | 把执行单元重定为对话、三态队列、键值地址树、tool_calls 协议不变量 | `CONTEXT.md` 术语表逐条对应 |
| 22 | 内存通道上做权限隔离 | `docs/capabilities.md` |
| 23 | 10 条原语指令 | `docs/runtime.md`：工具面「始终是全量 10 条」 |
| 23 | 10,878 行 Python | `find avm -name "*.py" \| xargs wc -l` |
| 23 | 970 个用例 | `python -m pytest tests/ --collect-only -q` → `970 tests collected` |
| 23 | 四组合 CI（Ubuntu/Windows × 3.12/3.13） | `.github/workflows/tests.yml` 的 matrix |
| 20 | 「亚对话不可信、只省 token」与「误差是调节不是消除」 | `CONTEXT.md`「亚对话」；`docs/philosophy.md` 六 |

---

## 一、规模与状态（第 23 行）

```
$ git log -1 --format="%h %ad %s" --date=iso
9ee2940 2026-11-03 16:38:47 +0800 docs(readme): 首屏给出一个镜像的真实骨架与项目状态

$ find avm -name "*.py" | xargs wc -l | tail -1
 10878 total

$ python -m pytest tests/ --collect-only -q | tail -1
970 tests collected in 2.02s

$ grep -n matrix -A4 .github/workflows/tests.yml
    matrix:
      os: [ubuntu-latest, windows-latest]
      python: ["3.12", "3.13"]
```

---

## 二、那次重构（第 22 行，commit `9ad13c2`）

```
$ git show --numstat --format="" 9ad13c2
2	2	avm/__init__.py
268	685	avm/core.py
26	79	avm/debug_utils.py
4	2	main.py
8	18	web/monitor_state.py
3	1	web/server.py
11	25	web/templates/monitor.html
```

日期 2026-07-25。core.py 净减 417 行，是把递归栈那套换成新骨架的那一刀。

---

## 三、文档里被引用的两处

### `CONTEXT.md`「亚对话」（第 20 行）

> 通过 `create_sub` 指令创建的新对话。亚对话被父对话的提示词决定和控制，父子紧耦合。亚对话在功能上不可信（父可注入提示词导致过度附合或过度批判），仅用于父对话节省 token，非用于任务执行。

### `docs/philosophy.md` 六「误差是调节，不是消除」（第 20 行）

> 软件工程假设：错误来自组件不正确，要在组合前用协议消除它。控制论假设：误差是系统的固有属性，无法消除，只能调节。
>
> AVM 不做"消除奇怪"，它用隔离、调度、预算中断、capability 寻址把误差关在可控范围内，再用元编程和多样性把它转化为产能。

---

## 四、复核命令

```bash
cd D:/ComputerST/Code/Project/AVM1
git remote -v
git log -1 --format="%h %ad" --date=iso
git show --numstat --format="" 9ad13c2
find avm -name "*.py" | xargs wc -l | tail -1
python -m pytest tests/ --collect-only -q | tail -1
```
