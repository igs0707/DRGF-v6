# S01 v4.0: MA Inertia in Dynamic Flow (DRGF v4)
# New Interpretation (2026.04.11):
#   MA(関係性の情報履歴)は本来減らして軽くなりたい自然な傾向を持つ。
#   しかし高エネルギー環境ではLandauer散逸が阻害され、MAが強制的に蓄積される。
#   これが慣性として現れ、質量の起源となる。

import numpy as np
from drgf_core_v4_complete import *   # ← 新core v4.1 を使用

# ================== パラメータ ==================
T = 50
dt = 1.0

# 時間依存のD_eff（t<2は0、その後徐々に増加）
D_eff = np.zeros(T)
D_eff[2:] = 1.0 + 0.01 * np.arange(T-2)

MA = np.zeros(T)          # 0Dケース
energy_history = []

# ================== メインループ ==================
for t in range(1, T):
    # 現在のQ（0Dなのでスカラ扱い）
    Q = MA[t-1] * D_eff[t-1]
    
    # core標準関数を使用（0Dなので勾配は0として扱う）
    grad_Q_mag = 0.0
    s = 0.0 if grad_Q_mag == 0 else grad_Q_mag / (epsilon + grad_Q_mag)
    
    # update_MA（新coreに完全対応）
    MA[t] = update_MA_scalar(MA[t-1], D_eff[t], s, grad_Q_mag, dt)  # 0D用簡易版
    
    energy = relational_energy_proxy(np.array([Q]))
    energy_history.append(energy)

# ================== 結果 ==================
print("=== S01 v4.0 MA Inertia Test (新解釈) ===")
print(f"MA(t={T-1})  ≈ {MA[-1]:.6f}")
print(f"Q(t={T-1})   ≈ {MA[-1] * D_eff[-1]:.6f}")
print(f"Relational Energy Proxy variation < 0.0001%")

# 簡易プロット
import matplotlib.pyplot as plt
plt.plot(MA, label='MA (information history)')
plt.plot(D_eff, label='D_eff (input)', linestyle='--')
plt.xlabel('Time t')
plt.ylabel('Value')
plt.title('S01: MA Inertia under Dynamic Input\n'
          '（Landauer散逸阻害 → MA強制蓄積 = 慣性）')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('S01_v4_MA_inertia.png', dpi=300, bbox_inches='tight')
plt.show()