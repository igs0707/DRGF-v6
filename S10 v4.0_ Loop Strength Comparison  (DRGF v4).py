# S10 v4.0: Loop Strength Comparison (DRGF v4)
# New Interpretation (2026.04.11):
#   MA(関係性の情報履歴)は本来減らして軽くなりたい自然な傾向を持つ。
#   しかし高エネルギー環境ではLandauer散逸が阻害され、MAが強制的に蓄積される。
#   Loop strengthの違いによりLife-like sustained growthからBlack Holeのrapid saturationまでを分類。

import numpy as np
import matplotlib.pyplot as plt
from drgf_core_v4_complete import *   # ← 新core v4.1 を使用

# ================== パラメータ ==================
T = 14000
dt = 1.0
gamma_small = 1e-7

# 4つのケース：Life / Star / Galaxy / Black Hole
cases = ['Life', 'Star', 'Galaxy', 'Black Hole']
growth_rates = [0.0012, 0.0008, 0.0005, 0.0002]   # Relation MA成長率
sat_strengths = [0.3, 0.8, 1.5, 3.0]               # saturationの強さ

# 結果保存
MA_r_hist = {case: np.zeros(T) for case in cases}
MA_p_hist = {case: np.zeros(T) for case in cases}

for idx, case in enumerate(cases):
    D_p = np.zeros(T)
    D_r = np.zeros(T)
    MA_p = np.zeros(T)
    MA_r = np.zeros(T)
    
    for t in range(T):
        D_p[t] = 0.6 * np.exp(-t / 12000) + 0.03 * np.sin(0.005 * t)
        D_r[t] = 0.4 * (1 + growth_rates[idx] * t) + 0.03 * np.sin(0.005 * t)
    
    for t in range(1, T):
        # Personal MA update
        Q_p = MA_p[t-1] * D_p[t-1]
        MA_p[t] = update_MA_scalar(MA_p[t-1], D_p[t], 0.0, 0.0, dt)
        
        # Relation MA update with saturation
        MA_total = MA_p[t-1] + MA_r[t-1]
        D_r_eff = D_r[t] / (1.0 + sat_strengths[idx] * MA_total)
        Q_r = MA_r[t-1] * D_r_eff
        MA_r[t] = update_MA_scalar(MA_r[t-1], D_r_eff, 0.0, 0.0, dt)
    
    MA_r_hist[case] = MA_r
    MA_p_hist[case] = MA_p

# ================== 結果 ==================
print("=== S10 v4.0 Loop Strength Comparison (新解釈) ===")
for case in cases:
    ratio = MA_r_hist[case][-1] / MA_p_hist[case][-1]
    print(f"{case:11s} → Relation / Personal ≈ {ratio:.1f} ×")

print("\n→ Strong loop (Life): sustained linear growth")
print("→ No loop (Black Hole): rapid saturation then decline")
print("→ Landauer散逸阻害によるMA強制蓄積がloop strengthの違いを生む")

# プロット
plt.figure(figsize=(10,6))
for case in cases:
    plt.plot(MA_r_hist[case], label=case)
plt.xlabel('Time t')
plt.ylabel('Relation MA')
plt.title('S10: Loop Strength Comparison\n'
          '（Landauer散逸阻害 → Life-like sustained growth vs Black Hole saturation）')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('S10_v4_loop_strength_comparison.png', dpi=300, bbox_inches='tight')
plt.show()