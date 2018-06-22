import numpy as np
from scipy.constants import epsilon_0, hbar, k






def Kerr_effect_nbar(P_in, kappa_0, kappa_ex, omega_c, omega_drive, K):
    
    Delta = omega_drive - omega_c
    
    kappa = kappa_ex + kappa_0
    
    p = [K**2, 2 * K * Delta, Delta**2 + (kappa/2)**2, - kappa_ex * P_in/hbar/(omega_c + Delta)]
    
    
    r = np.roots(p)
        
    # only get real solutions
    r = r[np.isreal(r)]
        
    nbar_min = min(np.real(r))
    
    return nbar_min
    
    
    
def optomechanics(P_in, kappa_0, kappa_ex, omega_c, omega_drive, omega_m, g_0):
    
    K = 2* g_0**2 / omega_m
    
    nbar = Kerr_effect_nbar(P_in, kappa_0, kappa_ex, omega_c, omega_drive, K)
    
    
    return {'omega_c': omega_c - K * nbar, 'g': g_0 * np.sqrt(nbar)}
    