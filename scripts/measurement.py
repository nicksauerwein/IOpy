import numpy as np
from scipy.constants import epsilon_0, hbar, k


class MeasurementOperator:
    
    def __init__(self, Q, system):
        
        self.system = system
        self.Q = Q
        

class PowerMeasurement:
    
    def __init__(self, output):
        
        self.system = output.system
        
        r = np.argwhere(output.system.inputs == output.input)[0,0]
        
        n = len(output.system.inputs)
        
        self.Q = np.zeros((2*n,2*n), dtype = 'complex128')
        
        self.Q[2*r, 2*r] = 1
        self.Q[2*r, 2*r+1] = 1j
        
        self.Q[2*r + 1, 2*r + 1] = 1
        self.Q[2*r + 1, 2*r] = -1j
        
class HomodynMeasurement:
    
    def __init__(self, output, theta):
        
        self.system = output.system
        
        r = np.argwhere(output.system.inputs == output.input)[0,0]
        
        n = len(output.system.inputs)
        
        self.Q = np.zeros((2*n,2*n), dtype = 'complex128')
        
        self.Q[2*r, 2*r] = np.cos(theta)**2
        self.Q[2*r, 2*r+1] = np.cos(theta)*np.sin(theta)
        self.Q[2*r + 1, 2*r + 1] = np.sin(theta)**2
        self.Q[2*r+1, 2*r] = np.cos(theta)*np.sin(theta)
        



def spectrum(omega, measurement, omega_rot = 0, components = False):
    
    omega = - omega + omega_rot
    system = measurement.system
    
    S1 = system.SMatrix(omega)
    S2 = np.conjugate(S1) #system.SMatrix(-omega)
    
    ni = int(S1.shape[1]/2)
    
    lo = len(omega)
    
    Q = measurement.Q
    
    #spec = np.zeros((2*ni,2*ni,2*ni), dtype = 'complex128')
    #specQ = np.zeros((2*ni,2*ni), dtype = 'complex128')
    
    res  = np.zeros((lo, 2*ni), dtype = 'complex128')
    
    for i in range(2*ni):
        for j in range(2*ni):
            if Q[i, j] == 0:
                pass
            
            #classical term
            #spec[i, j] = Q[i,j] * np.array([S1[i,k] * S2[j,k] * system.inputs[int(k/2)].spectrum(omega) for k in range(2*ni)])
            
            res += Q[i,j] * np.array([S1[:,i,k] * S2[:,j,k] * system.inputs[int(k/2)].spectrum(omega) for k in range(2*ni)]).T
            
            #spec[i, j] += Q[i,j] * np.array([S1[i,k] * S2[j,k] * (system.inputs[int(k/2)].spectrum(omega) - 0.25) for k in range(2*ni)])
            #quantum term
            
            #specQ[i, j] = Q[i,j] * 1j/2 * np.sum([(S2[i,2*r] * S1[j,2*r+1] - S2[i,2*r + 1] * S1[j,2*r])  for r in range(ni)])
    
    #res = np.sum(np.sum(spec,axis = 0), axis = 0)
    
    #resQ = np.sum(np.sum(specQ))
    #res = np.append(res, resQ)
    
    if components:
        return np.real (np.cumsum(res, axis = -1))
    
    return  np.real(np.sum(res, axis = -1)) #* hbar * (omega + output.input.omega_drive)

#spectrum = np.vectorize(spectrum)