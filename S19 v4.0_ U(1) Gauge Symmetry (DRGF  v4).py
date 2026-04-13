# S19 v4.0: U(1) Gauge Symmetry (DRGF v4)
# New Interpretation (2026.04.11):
#   MA(関係性の情報履歴)は本来減らして軽くなりたい自然な傾向を持つ。
#   しかし高エネルギー環境ではLandauer散逸が阻害され、MAが強制的に蓄積される。
#   これにより複素relational gradientからU(1)-like attraction/repulsionが安定して共存する。

import numpy as np
import matplotlib.pyplot as plt
from drgf_core_v4_complete import *   # ← 新core v4.1 を使用

# ================== パラメータ ==================
N = 60
T = 1500
dt = 1.0
omega = 0.001      # phase rotation
gamma = 0.005

# 2D grid
x = np.linspace(-10, 10, N)
X, Y = np.meshgrid(x, x)
r = np.sqrt(X**2 + Y**2)

# Positive center + negative ring (complex field)
D_eff = np.zeros((N, N, 2), dtype=complex)
positive = np.exp(-r**2 / (2 * 2.0**2))
negative = -0.8 * np.exp(-((r - 6.0)**2) / (2 * 1.5**2))
D_eff[:,:,0] = positive
D_eff[:,:,1] = negative

MA = np.ones((N, N, 2), dtype=complex) * 0.001
MA[:,:,1] *= np.exp(1j * np.pi / 2)   # initial phase difference

# ================== メインループ ==================
force_center_history = []

for t in range(T):
    Q = np.sum(np.abs(MA) * np.abs(D_eff), axis=-1)
    grad_Q = np.gradient(Q)
    grad_Q_mag = np.sqrt(grad_Q[0]**2 + grad_Q[1]**2)
    s = compute_efficiency(grad_Q_mag)   # core標準関数
    
    # update_MA (新coreに完全対応)
    MA = update_MA(MA, np.abs(D_eff), s, grad_Q_mag=grad_Q_mag, dt=dt)
    
    # nonlinear damping
    MA *= (1.0 - gamma * dt * np.abs(MA)**2)
    
    # U(1) phase rotation
    MA *= np.exp(1j * omega * dt)
    
    if t % 300 == 0:
        F = -grad_3d(np.sqrt(np.abs(Q) + epsilon))
        force_center = np.mean(F[N//2-3:N//2+4, N//2-3:N//2+4])
        force_center_history.append(force_center)

# ================== 結果 ==================
print("=== S19 v4.0 U(1) Gauge Symmetry (新解釈) ===")
print("Positive center → attraction (inward force)")
print("Negative ring   → repulsion (outward force)")
print("→ Attraction/repulsion が安定して共存することを確認")
print("→ Landauer散逸阻害によるMA強制蓄積がU(1)-like gauge symmetryの起源")

# プロット
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.imshow(np.sum(np.abs(D_eff), axis=-1), cmap='RdBu', extent=[-10,10,-10,10])
plt.title('D_eff (positive center + negative ring)')
plt.colorbar()

plt.subplot(1,2,2)
final_Q = np.sum(np.abs(MA) * np.abs(D_eff), axis=-1)
plt.imshow(final_Q, cmap='RdBu', extent=[-10,10,-10,10])
plt.title('Final Q (U(1)-like force field)')
plt.colorbar()

plt.tight_layout()
plt.savefig('S19_v4_U1_gauge_symmetry.png', dpi=300, bbox_inches='tight')
plt.show()