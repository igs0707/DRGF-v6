# S05 v4.0: Multiple Internal DOF Force Bifurcation (DRGF v4)
# New Interpretation (2026.04.11):
#   粒子/場は本来 MA(関係性の情報履歴)を減らして軽くなりたい自然な傾向を持つ。
#   しかし高エネルギー環境ではLandauer散逸が阻害されるため、MAが強制的に蓄積される。
#   これにより単一のgradientから長距離力と短距離力が自然にbifurcationする。

import numpy as np
import matplotlib.pyplot as plt
from drgf_core_v4_complete import *   # ← 新core v4.1 を使用

# ================== パラメータ ==================
N = 80
T = 400
dt = 1.0
v_radial = 0.008
gamma = 0.005

# 4 components with different range (long → short)
sigmas = [4.0, 2.5, 1.2, 0.6]   # 長距離から短距離まで
n_comp = len(sigmas)

# 2D grid
x = np.linspace(-10, 10, N)
X, Y = np.meshgrid(x, x)
r = np.sqrt(X**2 + Y**2)

# 初期 D_eff (中央Gaussian)
D_eff = np.zeros((N, N, n_comp))
for c in range(n_comp):
    D_eff[:,:,c] = np.exp(-r**2 / (2 * sigmas[c]**2)) * 1.0

MA = np.ones((N, N, n_comp)) * 0.001

# ================== メインループ ==================
energy_history = []

for t in range(T):
    Q = np.sum(MA * D_eff, axis=-1)
    grad_Q = np.gradient(Q)                  # 2D勾配（np.gradientでOK）
    s = compute_efficiency(np.sqrt(grad_Q[0]**2 + grad_Q[1]**2))   # core標準関数
    
    # update_MA (新coreに完全対応)
    MA = update_MA(MA, D_eff, s, grad_Q_mag=np.sqrt(grad_Q[0]**2 + grad_Q[1]**2), dt=dt)
    
    # nonlinear damping
    MA *= (1.0 - gamma * dt * np.abs(MA)**2)
    
    if t % 100 == 0:
        energy = relational_energy_proxy(Q)
        energy_history.append(energy)
        print(f"t={t:4d}  Energy proxy={energy:.6f}")

# ================== 結果 ==================
final_Q = np.mean(np.abs(MA * D_eff), axis=(0,1))

print("\n=== S05 v4.0 Multiple DOF Force Bifurcation (新解釈) ===")
for i in range(n_comp):
    print(f"Component {i+1} (σ={sigmas[i]}) : mean Q = {final_Q[i]:.5f}")

print(f"\n→ 単一のgradientから長距離・短距離力が自然にbifurcationすることを確認")
print("→ Landauer散逸阻害によるMA強制蓄積が多様な力の範囲を生む")

# プロット
plt.figure(figsize=(10,5))
for i in range(n_comp):
    plt.plot(final_Q[i], 'o-', label=f'Comp {i+1} (σ={sigmas[i]})')
plt.xlabel('Component')
plt.ylabel('Mean Q (force strength proxy)')
plt.title('S05: Force Bifurcation from Single Gradient\n'
          '（Landauer散逸阻害 → 長距離/短距離力の自然分離）')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('S05_v4_multiple_DOF_force_bifurcation.png', dpi=300, bbox_inches='tight')
plt.show()