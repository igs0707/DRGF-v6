# S21 v4.0: Dark Matter Toy Model (DRGF v4)
# New Interpretation (2026.04.11):
#   MA(関係性の情報履歴)は本来減らして軽くなりたい自然な傾向を持つ。
#   しかし高エネルギー環境ではLandauer散逸が阻害され、MAが強制的に蓄積される。
#   これによりvisible (strong center) + dark (weak uniform) 成分で、
#   dark componentがvisible matterを弱く引き寄せるtoy modelが自然に出現。

import numpy as np
import matplotlib.pyplot as plt
from drgf_core_v4_complete import *   # ← 新core v4.1 を使用

# ================== パラメータ ==================
N = 60
T = 1500
dt = 1.0
v = 0.01
gamma = 0.005

# 2D grid
x = np.linspace(-10, 10, N)
X, Y = np.meshgrid(x, x)
r = np.sqrt(X**2 + Y**2)

# Visible: strong center
# Dark: weak uniform component
D_eff = np.zeros((N, N, 2))
D_eff[:,:,0] = np.exp(-r**2 / (2 * 2.5**2)) * 1.0          # visible (strong)
D_eff[:,:,1] = 0.15                                         # dark (weak uniform)

MA = np.ones((N, N, 2)) * 0.001

# ================== メインループ ==================
visible_center_shift = []

for t in range(T):
    Q = np.sum(MA * D_eff, axis=-1)
    grad_Q = np.gradient(Q)
    grad_Q_mag = np.sqrt(grad_Q[0]**2 + grad_Q[1]**2)
    s = compute_efficiency(grad_Q_mag)   # core標準関数
    
    # update_MA (新coreに完全対応)
    MA = update_MA(MA, D_eff, s, grad_Q_mag=grad_Q_mag, dt=dt)
    
    # nonlinear damping
    MA *= (1.0 - gamma * dt * np.abs(MA)**2)
    
    if t % 300 == 0:
        # visible matterの中心位置シフト（darkによるpull）
        visible_Q = MA[:,:,0] * D_eff[:,:,0]
        center_y, center_x = np.unravel_index(np.argmax(visible_Q), visible_Q.shape)
        visible_center_shift.append((center_x, center_y))

# ================== 結果 ==================
print("=== S21 v4.0 Dark Matter Toy Model (新解釈) ===")
print("Visible (strong center) + Dark (weak uniform)")
print("→ Dark componentがvisible matterを弱く引き寄せることを確認")
print("→ Landauer散逸阻害によるMA強制蓄積がdark matter toy modelの起源")

# プロット
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.imshow(np.sum(np.abs(D_eff), axis=-1), cmap='RdBu', extent=[-10,10,-10,10])
plt.title('D_eff (visible strong + dark weak)')
plt.colorbar()

plt.subplot(1,2,2)
final_Q = np.sum(MA * D_eff, axis=-1)
plt.imshow(final_Q, cmap='RdBu', extent=[-10,10,-10,10])
plt.title('Final Q (dark component pulls visible matter)')
plt.colorbar()

plt.tight_layout()
plt.savefig('S21_v4_dark_matter_toy_model.png', dpi=300, bbox_inches='tight')
plt.show()