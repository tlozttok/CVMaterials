# CA / 条纹那条线：仓库存档

根目录：`D:\ComputerST\Code\Project\stripes_ca`
三个子项目：`life-ca`（振荡器本体）、`ca-initlab`（形态与拓扑实验）、`physa-ca`（生长机制目录）

简历第 30、32 行末尾的 `[ba2e4cf8、life-ca、ca-initlab、physa-ca]` 指的是这三个目录；`ba2e4cf8` 是那次对话的语料（4 条人侧消息，见 `../片段/L30-1_ba2e4cf8.md`），**不是**技术证据。技术证据全在这里。

---

## 一句一句对到文件

| 简历里的句子 | 文件 | 行 | 原文/数据 |
|---|---|---|---|
| 宏观斑图是步长太粗的假象 | `life-ca/MATH_ANALYSIS.md` | 7、104、124 | 「v2 找到的宏观图案也随步长细分一起消失……那批宏观图案和周期 2 是同一个离散伪影」 |
| 顶点判据量的是阈值，不是画面 | `ca-initlab/experiments/topo_graph/README.md` | 138–146 | disc 靶波 t=380 与 t=392 两帧，旧口径输出**完全相同**：`V=5 E=4 N1=4 N3=1 C=1 b1=0`；机理是 `mask_from_h` 用全域 `percentile(h,50)`，disc 只占 22% 面积 |
| 拓扑不变量 = 连通分量数减环数的两倍 | `ca-initlab/experiments/topology_algebra/README.md` | 12、15 | 「端点 (+1/2)、Y 三叉 (−1/2)、X 四叉 (−1) 的电荷和**不是 0，而是 2χ = 2(连通分量数 − 环数)**」；实测 −66.9 ± 24.3 vs 精确 2χ = −62.8 |
| 顶点不是能跟踪的对象 | `topo_graph/README.md` §3.3 | 103–105 | 寿命中位 **4 回合**，只有 0.09 个振荡周期（T=43）——注意这条本身是全局阈值切出来的假象（见 4b），简历里只写「不能跟踪」，没写数字，是对的 |
| 同相熔接、反相不熔接 | `ca-initlab/experiments/phase_relay/README.md` | 11 | 同相 → 100% 熔接（4/4，开闸后 7–10 回合）；反相 → 0%（0/2，200 回合内不熔接）；过渡带 2/6 |
| 或门成立、与门不成立 | `ca-initlab/experiments/logic_gate/README.md` | 65–70 | 「门类型 = OR；`(1,1)` 的强度没有翻倍（1.195 vs 1.196）」「AND 扫描：没有临界点」；24 组腔室×D×幅度无临界 |
| 稳定态下直接看到缺陷与条纹出现 | `ca-initlab/experiments/topo_graph/exp2_morpho.py`；`README.md` 189 | 189、206 | 「形态发生（单核 → 条纹海）」；「成核：`N3(t)` 是连续长还是跳变？（exp2 显示是**成批出现**）」 |
| 二十几种机制里只剩一套 | `physa-ca/CATALOG.md` | 13、32 | 速查表共 **22** 条机制；`D2｜脉冲扩张−张力收缩` 一栏写「**会长、会分叶**」并标「当前主线」 |

---

## 三个必须提醒的口径

1. **22 条不等于 22 条生长机制。** CATALOG 的 22 条里，A1–A4 是振荡器本体（基线、扩散扫描、偏置相变、薄膜/厚体），F1–F2 是初始条件对照，真正的生长律是 B、C、D、E 四组共 16 条。简历写「二十几种机制」按全部 22 条算，没错；但若面试官问「二十几种生长机制」，实际是 16 种。
2. **顶点寿命 4 回合不能用。** 它是全局阈值造成的莫尔斯分岔，109 次 births 里九成不是物理缺陷的生灭。所以简历只保留「不是能跟踪的对象」这个判断，数字全部删掉——这一点已经做对了。
3. **「逻辑门」是在冻结的 h 波导里搭的**（墙 h=5.6、通道 h=3.6），不是自然条纹自己长出的 Y 结。若被追问「这算不算这个系统本身能计算」，如实说：这是在该介质上人为构造的波导，用来测「这个介质支不支持逻辑」，不是系统自发涌现的门。

---

## 复核

```bash
cd D:/ComputerST/Code/Project/stripes_ca
sed -n '136,148p' ca-initlab/experiments/topo_graph/README.md   # 阈值失效
sed -n '10,20p'   ca-initlab/experiments/topology_algebra/README.md  # 电荷和
sed -n '60,75p'   ca-initlab/experiments/logic_gate/README.md   # OR / AND
sed -n '8,14p'    ca-initlab/experiments/phase_relay/README.md  # 同相/反相
sed -n '1,45p'    physa-ca/CATALOG.md                            # 22 条机制
sed -n '100,130p' life-ca/MATH_ANALYSIS.md                        # 步长伪影
```
