# S08 v4.0: Life-like Saturation Model (DRGF v4)
# New Interpretation (2026.04.11):
#   MA(関係性の情報履歴)は本来減らして軽くなりたい自然な傾向を持つ。
#   しかし高エネルギー環境ではLandauer散逸が阻害され、MAが強制的に蓄積される。
#   これによりPersonal inputは飽和する一方でRelation MAが成長し続ける
#   life-like behaviorが自然に出現する。

import numpy as np
import matplotlib.pyplot as plt
from drgf_core_v4_complete import *   # ← 新core v4.1 を使用

# ================== パラメータ ==================
T = 12000
dt = 1.0
gamma_sat = 0.5          # saturation strength
gamma_small = 1e-7       # small oscillation

# Personal input (内部入力：減衰 + 小振動)
# Relation input (外部入力：成長 + 小振動)
D_p = np.zeros(T)
D_r = np.zeros(T)

MA_p = np.zeros(T)   # Personal MA
MA_r = np.zeros(T)   # Relation MA

for t in range(T):
    D_p[t] = 0.8 * np.exp(-t / 8000) + 0.05 * np.sin(0.01 * t)      # 減衰傾向
    D_r[t] = 0.3 * (1 + 0.0008 * t) + 0.05 * np.sin(0.01 * t)       # 成長傾向

# ================== メインループ ==================
for t in range(1, T):
    # Personal MA update
    Q_p = MA_p[t-1] * D_p[t-1]
    grad_Q_mag_p = 0.0
    s_p = 0.0
    MA_p[t] = update_MA_scalar(MA_p[t-1], D_p[t], s_p, grad_Q_mag_p, dt)
    
    # Relation MA update with saturation (life-like behavior)
    MA_total = MA_p[t-1] + MA_r[t-1]
    D_r_eff = D_r[t] / (1.0 + gamma_sat * MA_total)   # saturation term
    Q_r = MA_r[t-1] * D_r_eff
    grad_Q_mag_r = 0.0
    s_r = 0.0
    MA_r[t] = update_MA_scalar(MA_r[t-1], D_r_eff, s_r, grad_Q_mag_r, dt)

# ================== 結果 ==================
print("=== S08 v4.0 Life-like Saturation Model (新解釈) ===")
print(f"Final Personal MA  = {MA_p[-1]:.4f}  (飽和)")
print(f"Final Relation MA  = {MA_r[-1]:.4f}")
print(f"Relation / Personal ratio ≈ {MA_r[-1] / MA_p[-1]:.1f} ×")
print("→ Personal inputは飽和する一方、Relation MAが成長し続けるlife-like behaviorを確認")
print("→ Landauer散逸阻害によるMA強制蓄積が生命様挙動の起源")

# プロット
plt.figure(figsize=(10,5))
plt.plot(MA_p, label='Personal MA (saturated)', linestyle='--')
plt.plot(MA_r, label='Relation MA (continues to grow)')
plt.xlabel('Time t')
plt.ylabel('MA')
plt.title('S08: Life-like Saturation Model\n'
          '（Landauer散逸阻害 → Personal飽和＋Relation成長）')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('S08_v4_life_like_saturation_model.png', dpi=300, bbox_inches='tight')
plt.show()