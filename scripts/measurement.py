import numpy as np
from scipy.constants import epsilon_0, hbar, k

def spectrum(output, omega):
    
    omega = - omega + output.input.omega_drive
    
    S1 = output.system.SMatrix(omega)
    S2 = output.system.SMatrix(-omega)
    
    
    ni = int(len(S1)/2)
    
    r = np.argwhere(output.system.inputs == output.input)[0,0]
    
    res1 = sum([ S1[2*r+1,2*k+1] * S2[2*r, 2*k] * output.system.inputs[k].spectrum(omega) for k in range(ni)] +
              [ S1[2*r+1,2*k] * S2[2*r, 2*k+1] * (output.system.inputs[k].spectrum(-omega) +1) for k in range(ni)])
    
    res2 = sum([ S2[2*r+1,2*k+1] * S1[2*r, 2*k] * output.system.inputs[k].spectrum(-omega) for k in range(ni)] +
              [ S2[2*r+1,2*k] * S1[2*r, 2*k+1] * (output.system.inputs[k].spectrum(omega) +1) for k in range(ni)])
    
    return  np.real(res1) #* hbar * (omega + output.input.omega_drive)

def homodyning(output, omega, angle):
    
    return 0
    