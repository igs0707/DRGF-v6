# drgf_core_v4_complete.py v4.2 (2026.04.11)
# DRGF v4 Unified Core - Final
# New Interpretation: Landauer散逸阻害によるMA強制蓄積

import numpy as np

epsilon = 1e-12
lambda0 = 0.00005
tau = 15000.0

# 新解釈パラメータ
gamma_decay = 0.0008      # 自壊圧力（本来はMAを減らしたい傾向）
beta_homeo = 0.0015       # 恒常性（蓄積されたMAを守ろうとする力）
beta_gravity = 0.0008     # 重力干渉
gamma_inertia = 0.0012    # 慣性

def lambda_s(s):
    return lambda0 / (1 + s / tau)

def compute_efficiency(grad_Q):
    """grad_Qから局所的な効率 s を計算"""
    return np.abs(grad_Q) / (epsilon + np.abs(grad_Q))

def grad_2d(field):
    """2D勾配"""
    grad = np.zeros_like(field)
    grad[1:-1, :] = (field[2:, :] - field[:-2, :]) / 2.0
    grad[:, 1:-1] = (field[:, 2:] - field[:, :-2]) / 2.0
    return grad

def grad_3d(field):
    """3D勾配"""
    grad = np.zeros_like(field)
    grad[1:-1, :, :] = (field[2:, :, :] - field[:-2, :, :]) / 2.0
    grad[:, 1:-1, :] = (field[:, 2:, :] - field[:, :-2, :]) / 2.0
    grad[:, :, 1:-1] = (field[:, :, 2:] - field[:, :, :-2]) / 2.0
    return grad

def update_MA(MA, D_eff, s, grad_Q_mag=None, dt=1.0):
    """3D/2D用 標準update_MA"""
    if grad_Q_mag is None:
        grad_Q_mag = np.abs(grad_3d(np.sum(np.abs(MA) * np.abs(D_eff), axis=-1)))
    
    dMA = lambda_s(s) * (D_eff - MA) * (grad_Q_mag / (epsilon + grad_Q_mag))
    
    decay_term = -gamma_decay * MA * (1.0 / (1.0 + np.abs(D_eff)))
    homeo_term = beta_homeo * grad_Q_mag * (D_eff - MA)
    inertia_term = gamma_inertia * MA
    
    dMA += decay_term + homeo_term + inertia_term
    return MA + dt * dMA

def update_MA_scalar(MA, D_eff, s, grad_Q_mag=0.0, dt=1.0):
    """0D/1D用 scalar版（S01〜S23などで頻出）"""
    dMA = lambda_s(s) * (D_eff - MA) * (grad_Q_mag / (epsilon + grad_Q_mag))
    
    decay_term = -gamma_decay * MA * (1.0 / (1.0 + D_eff))
    homeo_term = beta_homeo * grad_Q_mag * (D_eff - MA)
    inertia_term = gamma_inertia * MA
    
    dMA += decay_term + homeo_term + inertia_term
    return MA + dt * dMA

def update_MA_complex(MA, D_eff, s, grad_Q_mag=None, dt=1.0):
    """複素MA用（S06, S13, S19, S20, S22, S24などで使用）"""
    if grad_Q_mag is None:
        grad_Q_mag = np.abs(grad_3d(np.sum(np.abs(MA) * np.abs(D_eff), axis=-1)))
    return update_MA(MA, D_eff, s, grad_Q_mag, dt)   # 複素数もそのまま演算可能

def relational_energy_proxy(Q):
    """関係エネルギー（質量の起源）"""
    sqrtQ = np.sqrt(np.abs(Q) + epsilon)
    grad_sqrtQ = grad_3d(sqrtQ) if len(Q.shape) == 3 else grad_2d(sqrtQ)
    return np.mean(0.5 * np.abs(grad_sqrtQ)**2 + 0.5 * Q**2)

print("drgf_core_v4_complete.py v4.2 loaded")
print("→ update_MA_scalar / update_MA_complex 正式追加")
print("→ grad_2d / grad_3d 統一")
print("→ 新解釈 (Landauer散逸阻害によるMA強制蓄積) 反映済み")