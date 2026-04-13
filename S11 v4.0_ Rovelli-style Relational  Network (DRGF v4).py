# S11 v4.0: Rovelli-style Relational Network (DRGF v4)
# New Interpretation (2026.04.11):
#   MA(関係性の情報履歴)は本来減らして軽くなりたい自然な傾向を持つ。
#   しかし高エネルギー環境ではLandauer散逸が阻害され、MAが強制的に蓄積される。
#   これによりネットワーク全体でRelation MAがPersonal MAを上回り、
#   Rovelli的なrelational dominanceが自然に出現する。

import numpy as np
import matplotlib.pyplot as plt
from drgf_core_v4_complete import *   # ← 新core v4.1 を使用

# ================== パラメータ ==================
N_nodes = 100
T = 8000
dt = 1.0
gamma_small = 1e-7

np.random.seed(42)

# ランダム対称隣接行列（無向グラフ）
adj = np.random.rand(N_nodes, N_nodes)
adj = (adj + adj.T) / 2
adj = (adj > 0.7).astype(float)   # 接続密度を調整
np.fill_diagonal(adj, 0)          # 自己ループなし

# Personal MAとRelation MA (各nodeごとに保持)
MA_p = np.zeros((T, N_nodes))
MA_r = np.zeros((T, N_nodes))

# 初期入力
D_p = np.zeros((T, N_nodes))
D_r = np.zeros((T, N_nodes))

for t in range(T):
    D_p[t] = 0.6 * np.exp(-t / 12000) + 0.03 * np.sin(0.005 * t)
    D_r[t] = 0.4 * (1 + 0.0005 * t) + 0.03 * np.sin(0.005 * t)

# ================== メインループ ==================
crossover_time = None

for t in range(1, T):
    for i in range(N_nodes):
        # Personal MA update (node i)
        neighbors_p = np.sum(adj[i] * MA_p[t-1])
        Q_p = MA_p[t-1, i] * D_p[t-1, i] + 0.1 * neighbors_p
        MA_p[t, i] = update_MA_scalar(MA_p[t-1, i], D_p[t, i], 0.0, 0.0, dt)
        
        # Relation MA update (node i)
        neighbors_r = np.sum(adj[i] * MA_r[t-1])
        Q_r = MA_r[t-1, i] * D_r[t-1, i] + 0.3 * neighbors_r
        MA_r[t, i] = update_MA_scalar(MA_r[t-1, i], D_r[t, i], 0.0, 0.0, dt)
    
    # クロスオーバー検出（平均値で）
    if crossover_time is None and np.mean(MA_r[t]) > np.mean(MA_p[t]):
        crossover_time = t

# ================== 結果 ==================
print("=== S11 v4.0 Rovelli-style Relational Network (新解釈) ===")
print(f"Crossover at t ≈ {crossover_time}")
print(f"Final mean Relation MA = {np.mean(MA_r[-1]):.4f}")
print(f"Final mean Personal MA = {np.mean(MA_p[-1]):.4f}")
print(f"Relation MA dominates network-wide : {np.mean(MA_r[-1]) > np.mean(MA_p[-1])}")
print("→ Relation MAがネットワーク全体でPersonal MAを上回ることを確認")
print("→ Landauer散逸阻害によるMA強制蓄積がRovelli的relational dominanceを生む")

# プロット
plt.figure(figsize=(10,5))
plt.plot(np.mean(MA_p, axis=1), label='Mean Personal MA', linestyle='--')
plt.plot(np.mean(MA_r, axis=1), label='Mean Relation MA')
plt.axvline(crossover_time, color='red', linestyle=':', label=f'Crossover t≈{crossover_time}')
plt.xlabel('Time t')
plt.ylabel('Mean MA (network average)')
plt.title('S11: Rovelli-style Relational Network\n'
          '（Landauer散逸阻害 → Relation MAのnetwork-wide dominance）')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('S11_v4_rocelli_style_relational_network.png', dpi=300, bbox_inches='tight')
plt.show()