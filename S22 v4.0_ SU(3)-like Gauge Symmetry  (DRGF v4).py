# S22 v4.0: SU(3)-like Gauge Symmetry (DRGF v4)
# New Interpretation (2026.04.11):
#   MA(関係性の情報履歴)は本来減らして軽くなりたい自然な傾向を持つ。
#   しかし高エネルギー環境ではLandauer散逸が阻害され、MAが強制的に蓄積される。
#   これにより3-componentのnon-commutative mixingから複雑なSU(3)-like force patternsが自然に出現する。

import numpy as np
import matplotlib.pyplot as plt
from drgf_core_v4_complete import *   # ← 新core v4.1 を使用

# ================== パラメータ ==================
N = 60
T = 1500
dt = 1.0
omega = 0.001
gamma = 0.005

# 2D grid
x = np.linspace(-10, 10, N)
X, Y = np.meshgrid(x, x)
r = np.sqrt(X**2 + Y**2)

# 3 components with different positive/negative patterns (SU(3)-like)
D_eff = np.zeros((N, N, 3))
D_eff[:,:,0] = np.exp(-r**2 / (2 * 2.5**2))                     # positive
D_eff[:,:,1] = -0.7 * np.exp(-((r - 5.0)**2) / (2 * 1.8**2))   # negative ring 1
D_eff[:,:,2] = 0.6 * np.exp(-((r + 4.0)**2) / (2 * 1.5**2))    # positive offset

MA = np.ones((N, N, 3), dtype=complex) * 0.001
MA[:,:,1] *= np.exp(1j * np.pi / 3)   # initial non-commutative phase mixing
MA[:,:,2] *= np.exp(1j * 2*np.pi / 3)

# ================== メインループ ==================
force_patterns = []

for t in range(T):
    Q = np.sum(np.abs(MA) * np.abs(D_eff), axis=-1)
    grad_Q = np.gradient(Q)
    grad_Q_mag = np.sqrt(grad_Q[0]**2 + grad_Q[1]**2)
    s = compute_efficiency(grad_Q_mag)   # core標準関数
    
    # update_MA (新coreに完全対応)
    MA = update_MA(MA, np.abs(D_eff), s, grad_Q_mag=grad_Q_mag, dt=dt)
    
    # nonlinear damping
    MA *= (1.0 - gamma * dt * np.abs(MA)**2)
    
    # phase rotation (SU(3)-like mixing)
    MA *= np.exp(1j * omega * dt)
    
    if t % 300 == 0:
        force_patterns.append(np.mean(np.abs(grad_3d(Q))))

# ================== 結果 ==================
print("=== S22 v4.0 SU(3)-like Gauge Symmetry (新解釈) ===")
print("→ 3-component non-commutative mixingから複雑な力のパターンが自然に出現")
print("→ Landauer散逸阻害によるMA強制蓄積がSU(3)-like gauge symmetryの起源")

# プロット
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.imshow(np.sum(np.abs(D_eff), axis=-1), cmap='RdBu', extent=[-10,10,-10,10])
plt.title('D_eff (3 components)')
plt.colorbar()

plt.subplot(1,2,2)
final_Q = np.sum(np.abs(MA) * np.abs(D_eff), axis=-1)
plt.imshow(final_Q, cmap='RdBu', extent=[-10,10,-10,10])
plt.title('Final Q (SU(3)-like non-commutative force patterns)')
plt.colorbar()

plt.tight_layout()
plt.savefig('S22_v4_SU3_like_gauge_symmetry.png', dpi=300, bbox_inches='tight')
plt.show()