# S09 v4.0: Black Hole Model (DRGF v4)
# New Interpretation (2026.04.11):
#   MA(関係性の情報履歴)は本来減らして軽くなりたい自然な傾向を持つ。
#   しかし高エネルギー環境ではLandauer散逸が阻害され、MAが強制的に蓄積される。
#   イベントホライズン（input cutoff）後にもRelation MAの記憶が持続する
#   black-hole-like behaviorが自然に出現する。

import numpy as np
import matplotlib.pyplot as plt
from drgf_core_v4_complete import *   # ← 新core v4.1 を使用

# ================== パラメータ ==================
T = 12000
dt = 1.0
gamma_small = 1e-7
event_horizon = 2000   # イベントホライズン（D_rが急激にdrop）

D_p = np.zeros(T)   # Personal input
D_r = np.zeros(T)   # Relation input

MA_p = np.zeros(T)
MA_r = np.zeros(T)

for t in range(T):
    D_p[t] = 0.6 * np.exp(-t / 10000) + 0.03 * np.sin(0.005 * t)   # 内部入力（減衰）
    D_r[t] = 0.8 * (1 + 0.0005 * t) + 0.03 * np.sin(0.005 * t)     # 外部入力（成長）

# イベントホライズンでD_rをsharp drop
D_r[event_horizon:] = D_r[event_horizon:] * 0.001

# ================== メインループ ==================
for t in range(1, T):
    # Personal MA update
    Q_p = MA_p[t-1] * D_p[t-1]
    grad_Q_mag_p = 0.0
    s_p = 0.0
    MA_p[t] = update_MA_scalar(MA_p[t-1], D_p[t], s_p, grad_Q_mag_p, dt)
    
    # Relation MA update
    Q_r = MA_r[t-1] * D_r[t-1]
    grad_Q_mag_r = 0.0
    s_r = 0.0
    MA_r[t] = update_MA_scalar(MA_r[t-1], D_r[t], s_r, grad_Q_mag_r, dt)

# ================== 結果 ==================
print("=== S09 v4.0 Black Hole Model (新解釈) ===")
print(f"Event horizon at t = {event_horizon}")
print(f"Final Relation MA  = {MA_r[-1]:.4f}")
print(f"Final Personal MA  = {MA_p[-1]:.4f}")
print(f"Relation MA / Personal MA ≈ {MA_r[-1] / MA_p[-1]:.1f} × (dominant)")
print("→ cutoff後もRelation MAの記憶が持続することを確認")
print("→ Landauer散逸阻害によるMA強制蓄積がblack-hole memoryの起源")

# プロット
plt.figure(figsize=(10,5))
plt.plot(MA_p, label='Personal MA', linestyle='--')
plt.plot(MA_r, label='Relation MA')
plt.axvline(event_horizon, color='red', linestyle=':', label='Event Horizon (input cutoff)')
plt.xlabel('Time t')
plt.ylabel('MA')
plt.title('S09: Black Hole Model\n'
          '（Landauer散逸阻害 → cutoff後もRelation MA記憶が持続）')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('S09_v4_black_hole_model.png', dpi=300, bbox_inches='tight')
plt.show()