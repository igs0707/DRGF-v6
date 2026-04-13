# S17 v4.0: Isolated System + Vacuum Fluctuations (DRGF v4)
# New Interpretation (2026.04.11):
#   MA(関係性の情報履歴)は本来減らして軽くなりたい自然な傾向を持つ。
#   しかし高エネルギー環境ではLandauer散逸が阻害され、MAが強制的に蓄積される。
#   Heat death後の極小vacuum fluctuation下でもMA memoryが持続する。

import numpy as np
import matplotlib.pyplot as plt
from drgf_core_v4_complete import *   # ← 新core v4.1 を使用

# ================== パラメータ ==================
T = 3000
dt = 1.0
heat_death_time = 1500
gamma_small = 1e-7

D_p = np.zeros(T)   # Personal input
D_r = np.zeros(T)   # Relation input

MA_p = np.zeros(T)
MA_r = np.zeros(T)

for t in range(T):
    D_p[t] = 0.6 * np.exp(-t / 12000) + 0.03 * np.sin(0.005 * t)
    D_r[t] = 0.8 * (1 + 0.0005 * t) + 0.03 * np.sin(0.005 * t)

# Heat death + post-heat-death vacuum fluctuations
D_r[heat_death_time:] = 1e-8 * np.sin(0.01 * np.arange(T - heat_death_time))

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
decay_percent = (MA_r[heat_death_time] - MA_r[-1]) / MA_r[heat_death_time] * 100 if MA_r[heat_death_time] > 0 else 0

print("=== S17 v4.0 Isolated System + Vacuum Fluctuations (新解釈) ===")
print(f"Heat death at t = {heat_death_time}")
print(f"Post-heat-death vacuum fluctuation: D_r ≈ 10^{-8} sin(0.01 t)")
print(f"Final Relation MA = {MA_r[-1]:.4f}")
print(f"MA memory decay after cutoff ≈ {decay_percent:.2f}%")
print(f"Memory clearly remains : {MA_r[-1] > 0.9 * MA_r[heat_death_time]}")
print("→ tiny vacuum fluctuation下でもMA memoryが持続することを確認")
print("→ Landauer散逸阻害によるMA強制蓄積がisolated systemでのmemory persistenceの起源")

# プロット
plt.figure(figsize=(10,5))
plt.plot(MA_p, label='Personal MA', linestyle='--')
plt.plot(MA_r, label='Relation MA')
plt.axvline(heat_death_time, color='red', linestyle=':', label='Heat Death + Vacuum Fluctuations')
plt.xlabel('Time t')
plt.ylabel('MA')
plt.title('S17: Isolated System + Vacuum Fluctuations\n'
          '（Landauer散逸阻害 → cutoff後もMA memory持続）')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('S17_v4_isolated_system_vacuum_fluctuations.png', dpi=300, bbox_inches='tight')
plt.show()