# -*- coding: utf-8 -*-
"""按简历里的 [cid/node] 引用，把语料切成片段。

用法：
    python 生成.py
会重写 `片段/` 与 `索引.csv`，并在终端报告：缺失节点、指向 AI 原文的节点。
简历改动后重跑一次即可，不需要手工维护片段。

数据源：deepseek_data-2026-11-03/conversations.json
节点号：原始导出里 mapping 的键，与简历方括号里的数字一致。
"""
import csv
import json
import os
import re

# 本脚本放在「引用材料包」里，上一级就是简历工作区。换机器时可用环境变量覆盖：
#   CV_ROOT   简历工作区根目录（含 final/ 与语料导出）
#   CV_CORPUS conversations.json 的完整路径
HERE = os.path.dirname(os.path.abspath(__file__))
CV = os.environ.get('CV_ROOT') or os.path.dirname(HERE)
CORP = os.environ.get('CV_CORPUS') or os.path.join(CV, 'deepseek_data-2026-11-03', 'conversations.json')
OUT = HERE
FR = os.path.join(OUT, '片段')
SRC = os.path.join(CV, 'final', '预终稿.txt')

CIT = re.compile(r'[0-9a-f]{8}')


def frag(m, t):
    return ''.join(f.get('content', '') for f in (m.get('fragments') or []) if f.get('type') == t)


def parse(body):
    """'a/3、9、b/1-5' -> [('a',[3,9]), ('b',[1,2,3,4,5])]"""
    raw, cur = [], None
    for tok in re.split(r'[、,，]\s*', body.strip()):
        m = re.fullmatch(r'([0-9a-f]{8})(?:/(\d+)(?:[-–](\d+))?)?', tok)
        if m:
            cur, a, b = m.group(1), m.group(2), m.group(3)
            if a is None:
                raw.append((cur, None))
            else:
                lo = int(a)
                hi = int(b) if b else lo
                raw.append((cur, list(range(lo, hi + 1))))
        elif re.fullmatch(r'\d+', tok) and cur:
            raw.append((cur, [int(tok)]))
    merged = []
    for cid, idxs in raw:
        if merged and merged[-1][0] == cid:
            prev = merged[-1][1]
            merged[-1] = (cid, None if (prev is None or idxs is None) else prev + idxs)
        else:
            merged.append((cid, idxs))
    return merged


def load_notes(text):
    """从文末「注释」块里读出 [n] -> 原始引用内容。"""
    m = re.search(r'\n注释\n', text)
    notes = {}
    if not m:
        return notes
    for line in text[m.end():].split('\n'):
        mm = re.fullmatch(r'\[(\d+)\]\s*(.+)', line.strip())
        if mm:
            notes[int(mm.group(1))] = mm.group(2)
    return notes


def main():
    os.makedirs(FR, exist_ok=True)
    for f in os.listdir(FR):
        os.remove(os.path.join(FR, f))

    data = json.load(open(CORP, encoding='utf-8'))
    conv = {c['id'][:8]: c for c in data}

    raw = open(SRC, encoding='utf-8').read()
    notes = load_notes(raw)
    body_part = raw.split('\n注释\n')[0]

    def expand(line):
        """把正文里的 [12] 换回 [eae12e37/9...]，注释块本身不参与扫描。"""
        return re.sub(r'\[(\d+)\]', lambda m: '[' + notes.get(int(m.group(1)), m.group(1)) + ']', line)

    lines = body_part.split('\n')
    brk = re.compile(r'\[([^\]]*)\]')
    rows, missing, ai_nodes = [], [], []

    for ln, line in enumerate(lines, 1):
        raw_line = line
        line = expand(line)
        k = 0
        for mo in brk.finditer(line):
            body = mo.group(1)
            if not CIT.search(body):
                continue
            pairs = parse(body)
            if not pairs:
                continue
            k += 1
            name = f'L{ln:02d}-{k}_{pairs[0][0]}.md'
            seg = [x for x in re.split(r'(?<=[。；！？])', line) if '[' + body + ']' in x]
            claim = seg[0].strip() if seg else line.strip()[:80]
            buf = [f'# L{ln:02d}-{k}｜`{body}`\n',
                   f'**出处** 最终稿第 {ln} 行\n',
                   f'**它支撑的那一句**  \n> {claim}\n\n---\n']
            cnt = 0
            for cid, idxs in pairs:
                c = conv.get(cid)
                if not c:
                    missing.append(cid)
                    buf.append(f'\n## `{cid}` 未找到\n')
                    continue
                span = f"{(c.get('inserted_at') or '')[:10]} → {(c.get('updated_at') or '')[:10]}"
                if idxs is None:
                    sel = [(n['message'].get('inserted_at') or '', nid, n['message'])
                           for nid, n in c['mapping'].items() if n.get('message')]
                    note = f'该会话全部 {len(sel)} 条'
                else:
                    sel = []
                    for i in dict.fromkeys(idxs):
                        n = c['mapping'].get(str(i))
                        if n and n.get('message'):
                            sel.append((n['message'].get('inserted_at') or '', str(i), n['message']))
                        else:
                            missing.append(f'{cid}/node {i}')
                    note = 'node ' + ','.join(str(i) for i in dict.fromkeys(idxs))
                sel.sort(key=lambda x: (x[0], x[1]))
                buf.append(f"\n## `{cid}` ｜ {c.get('title')}\n\n{note}｜{span}\n")
                for t, nid, m in sel:
                    u, a = frag(m, 'REQUEST'), frag(m, 'RESPONSE')
                    role = '用户' if u else ('AI' if a else '空')
                    if not u and a:
                        ai_nodes.append(f'L{ln}/node {nid}')
                    txt = (u or a).strip()
                    if not txt:
                        continue
                    cnt += 1
                    q = '\n'.join('> ' + x if x.strip() else '>' for x in txt.split('\n'))
                    buf.append(f'\n### node {nid} · {t[:16].replace("T", " ")} · {role}\n\n{q}\n')
            open(os.path.join(FR, name), 'w', encoding='utf-8').write('\n'.join(buf))
            txt = buf[0]
            rows.append({'line': ln, 'body': body, 'file': name, 'n': cnt,
                         'ai': txt.count('· AI'), 'claim': claim})

    # 逐文件回读一遍，统计用户/AI 条数（更可靠）
    table = []
    for r in rows:
        t = open(os.path.join(FR, r['file']), encoding='utf-8').read()
        u, a = t.count('· 用户'), t.count('· AI')
        note = []
        if '/' not in r['body']:
            note.append('整段会话')
        if a:
            note.append(f'含 {a} 条 AI 原文')
        table.append((r['line'], r['body'], r['file'], u, a, '；'.join(note)))

    with open(os.path.join(OUT, '索引.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['简历行', '引用', '片段文件', '本人原话条数', 'AI原文条数', '备注'])
        w.writerows(table)

    print(f'片段 {len(table)} 个｜节点 {sum(x[3] + x[4] for x in table)} 条')
    print('缺失:', missing or '无')
    print('指向 AI 原文的节点:', ai_nodes or '无')


if __name__ == '__main__':
    main()
