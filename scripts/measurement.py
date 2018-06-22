import numpy as np
from scipy.constants import epsilon_0, hbar, k

def spectrum(output, omega, components = False):
    
    omega = - omega + output.input.omega_drive
    
    S1 = output.system.SMatrix(omega)
    S2 = output.system.SMatrix(-omega)
    
    
    ni = int(len(S1)/2)
    
    r = np.argwhere(output.system.inputs == output.input)[0,0]
    
    res = (np.array([ S1[2*r+1,2*k+1] * S2[2*r, 2*k] * output.system.inputs[k].spectrum(omega) for k in range(ni)]) +
          np.array([ S1[2*r+1,2*k] * S2[2*r, 2*k+1] * (output.system.inputs[k].spectrum(-omega) +1) for k in range(ni)]))
    
    
    if components:
        return np.real (np.cumsum(res))
        
    
    
    
    return  np.real(res) #* hbar * (omega + output.input.omega_drive)

def homodyning(output, omega, angle):
    
    return 0
    