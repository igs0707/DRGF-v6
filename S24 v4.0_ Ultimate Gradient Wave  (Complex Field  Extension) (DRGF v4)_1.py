# S24 v4.0: Ultimate Gradient Wave (Complex Field Extension) (DRGF v4)
# New Interpretation (2026.04.11):
#   MA(関係性の情報履歴)は本来減らして軽くなりたい自然な傾向を持つ。
#   しかし高エネルギー環境ではLandauer散逸が阻害され、MAが強制的に蓄積される。
#   これにより古典的な波パラメータ(k, ωなど)を一切使わずに、
#   複素MAからgradient waveと位相伝播が純粋に創発する。

import numpy as np
import matplotlib.pyplot as plt
from drgf_core_v4_complete import *   # ← 新core v4.1 を使用

# ================== パラメータ ==================
N = 64
T = 300
dt = 1.0
gamma = 0.005

# 2D grid
x = np.linspace(-10, 10, N)
X, Y = np.meshgrid(x, x)
r = np.sqrt(X**2 + Y**2)

# 複素場 (D_effとMAの両方を複素化)
D_eff = np.ones((N, N), dtype=complex) * 0.05
# ε-scale gradient seeds (pre-Big-Bang residual)
D_eff += 1e-4 * (np.exp(1j * np.random.uniform(0, 2*np.pi, (N, N))) * np.exp(-r**2 / 8.0))

MA = np.ones((N, N), dtype=complex) * 0.0005
MA += 1e-5 * np.exp(1j * np.random.uniform(0, 2*np.pi, (N, N)))

# ================== メインループ ==================
amplitude_history = []
phase_history = []

for t in range(T):
    Q = np.abs(MA) * np.abs(D_eff)
    grad_Q = np.gradient(Q)
    grad_Q_mag = np.sqrt(grad_Q[0]**2 + grad_Q[1]**2)
    s = compute_efficiency(grad_Q_mag)   # core標準関数
    
    # update_MA (新coreに完全対応)
    MA = update_MA(MA, np.abs(D_eff), s, grad_Q_mag=grad_Q_mag, dt=dt)
    
    # nonlinear damping
    MA *= (1.0 - gamma * dt * np.abs(MA)**2)
    
    if t % 50 == 0:
        amplitude_history.append(np.mean(np.abs(MA)))
        phase_history.append(np.std(np.angle(MA)))

# ================== 結果 ==================
print("=== S24 v4.0 Ultimate Gradient Wave (Complex Field Extension) (新解釈) ===")
print("→ 古典的な波パラメータ(k, ωなど)を使わずに複素MAからgradient waveと位相伝播が純粋に創発")
print("→ Landauer散逸阻害によるMA強制蓄積がwave-like behaviorの起源")
print(f"Final amplitude mean ≈ {amplitude_history[-1]:.5f}")
print(f"Final phase std     ≈ {phase_history[-1]:.5f} rad")

# プロット
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.imshow(np.abs(MA), cmap='viridis', extent=[-10,10,-10,10])
plt.title('|MA| (Gradient Wave Amplitude)')
plt.colorbar()

plt.subplot(1,2,2)
plt.imshow(np.angle(MA), cmap='twilight', extent=[-10,10,-10,10])
plt.title('Phase (Natural Propagation)')
plt.colorbar()

plt.tight_layout()
plt.savefig('S24_v4_complex_gradient_wave_2d.png', dpi=300, bbox_inches='tight')
plt.show()