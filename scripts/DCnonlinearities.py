import numpy as np
from scipy.constants import epsilon_0, hbar, k


def Kerr_effect_nbar(P_in, kappa_0, kappa_ex, omega_c, omega_drive, K):
    '''
    This function findes the steady state average number of photons in an optical cavity with kerr type nonlinearity.
    It findes the smallest real route of a third order polynomial equation:
    
        a * n^3 + b * n^2 + c * n + d = 0
        a = - kappa_ex * P_in/hbar/(omega_drive)
        b = Delta**2 + (kappa/2)**2
        c = 2 * K * Delta
        d = K**2
        
    Args:
        P_in: input power in Watts.
        kappa_0 = cavity intrinsic dissipation rate in rad/sec.
        kappa_ex = input coupling rate in rad/sec.
        omega_c = cavity resonance frequency in rad/sec.
        omega_drive = frequency of the input field in rad/sec.
        K = nonlinearity coefficient in rad/sec.
        
    returns:
        nbar: smallest real route of the third order polynomial equation.
    '''
    Delta = omega_drive - omega_c
    
    kappa = kappa_ex + kappa_0
    
    p = [K**2, 2 * K * Delta, Delta**2 + (kappa/2)**2, - kappa_ex * P_in/hbar/(omega_c + Delta)]
    
    
    r = np.roots(p)
        
    # only get real solutions
    r = r[np.isreal(r)]
        
    nbar_min = min(np.real(r))
    
    return nbar_min
    
    
    
def optomechanics(P_in, kappa_0, kappa_ex, omega_c, omega_drive, omega_m, g_0):
    '''
    This function findes the steady state average number of photons in an optomechanical cavity and also finds the DC shift cavity 
    resonance frequency. It uses the Kerr_effect_nbar() function to solve the third order equation:
    
        n * ( kappa^2/4 + (Delta - (2g_0^2/omega_m) * n)^2 ) = kappa_ext * P_in / (hbar*omega_drive)
    
    Args:
        P_in: input power in Watts.
        kappa_0 = cavity intrinsic dissipation rate in rad/sec.
        kappa_ex = input coupling rate in rad/sec.
        omega_c = cavity resonance frequency in rad/sec.
        omega_drive = frequency of the input field in rad/sec.
        omega_m = resonance frequency of the mechanical oscillator in rad/sec.
        g_0 =  vacuum optomechanical coupling rate in rad/sec.
        
    returns:
        omega_c = modified cavity resonance frequency in rad/sec.
        g = optomechanical coupling rate in rad/sec.
    '''
    
    K = 2* g_0**2 / omega_m
    
    nbar = Kerr_effect_nbar(P_in, kappa_0, kappa_ex, omega_c, omega_drive, K)
    
    
    return {'omega_c': omega_c - K * nbar, 'g': g_0 * np.sqrt(nbar)}
    