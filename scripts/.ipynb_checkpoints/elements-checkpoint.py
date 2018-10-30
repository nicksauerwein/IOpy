import numpy as np
from scipy.constants import epsilon_0, hbar, k
#test
class Mode:
    def __init__(self,name, omega):
        self.name = name
        self.omega_rot = omega
        self.omega = omega
        self.kappa = 0
        
        self.driven = False
        
    def __str__(self):
        
        return self.name
        
class Input:
    def __init__(self,name, mode, kappa, kind = 'bath', omega_drive = 0, bath_temp = 0):
        '''
        possible kind of inputs:
            - drive: coherent drive
                The only reason why we need omega_drive is to go into the rotating frame
            - bath: vacuum or thermal
        '''
        self.name = name
        self.kappa = kappa
        self.kind = kind
        self.mode = mode
        
        self.mode.kappa += kappa
        
        if kind == 'drive':
            
            if mode.driven:
                raise ValueError('Mode '+mode.name+' is already driven! Connot go into rotating frame!')
            
            mode.driven = True
            mode.omega_rot = mode.omega - omega_drive
        
        self.omega_drive = omega_drive
        self.bath_temp = bath_temp

        if bath_temp == 0:
            self.nbar = 0
        else:
            
            self.nbar = 1/(np.exp(hbar * (mode.omega) / k / bath_temp) - 1)
        
    def spectrum(self, omega):
        return 0.5 * self.nbar + 0.25 * np.ones_like(omega)
    
    def __str__(self):
        
        return str(self.mode)+'_in,'+self.name
        
        

class Coupling:
    def __init__(self,mode1, mode2, vg):
        '''
        vg: coupling vector [real]
        
        H_int = 4 hbar ( vg[0] q1 q2 + vg[1] q1 p2 + vg[2] p1 q2 + vg[3] p1 p2)
        
        EXAMPLE
        For optomechanics:
        vg = [g , 0, 0, 0] 
        '''
        self.mode1 = mode1
        self.mode2 = mode2
        
        self.vg = vg
   
    def __str__(self):
        
        return 'g_'+str(mode1)+str(mode2)

        
        
    def contains_mode(self,mode):
        if mode1 == mode:
            True
        if mode2 == mode:
            True
            
        return False
            
        
        
class System:
    def __init__ (self, modes = [], inputs = [], couplings = []):
        self.modes = np.array(modes)
        self.inputs = np.array(inputs)
        self.couplings = np.array(couplings)
        
        self.make_ML()
        
    def add_mode(self,mode):
        np.append(self.modes ,mode)
        self.make_ML()
        
    def add_input(self,inp):
        np.append(self.inputs ,inp)
        self.make_ML()
        
    def add_coupling(self,coup):
        np.append(self.couplings ,coup)
        self.make_ML()
    
    def make_ML(self):
        nm = len(self.modes)
        ni = len(self.inputs)
        
        M = np.zeros((2 * nm, 2 * nm), dtype = 'complex')
        L = np.zeros((2 * ni, 2 * nm), dtype = 'complex')
        
        
        for i, inp in enumerate(self.inputs):
            j = np.argwhere(self.modes == inp.mode)
            
            L[2*i, 2*j] = np.sqrt(inp.kappa)
            L[2*i + 1, 2*j + 1] = np.sqrt(inp.kappa)
        
        for coupling in self.couplings:
            i = np.argwhere(self.modes == coupling.mode1)
            j = np.argwhere(self.modes == coupling.mode2)
            
            M[2*i,2*j] = 2 * coupling.vg[2]
            M[2*i + 1,2*j + 1] = - 2 * coupling.vg[1]
            M[2*i,2*j + 1] =  2 * coupling.vg[3]
            M[2*i + 1,2*j] = - 2 * coupling.vg[0]    
            
            M[2*j,2*i] =  2 * coupling.vg[1]
            M[2*j + 1,2*i + 1] = - 2 * coupling.vg[2]
            M[2*j,2*i + 1] = 2 * coupling.vg[3]
            M[2*j + 1,2*i] = - 2 * coupling.vg[0] 

            
        for i,mode in enumerate(self.modes):
            M[2*i,2*i] = - mode.kappa/2
            M[2*i + 1,2*i + 1] = - mode.kappa/2
            
            M[2*i,2*i + 1] = mode.omega_rot
            M[2*i + 1,2*i] = - mode.omega_rot
            
        self.M = M
        self.L = L
            
    def SMatrix(self, omegas):
        M = self.M
        L = self.L
        
        #lo = len(omegas)
        
        Ss = np.array([np.eye(len(L)) + L @ np.linalg.inv(1j * omega * np.eye(len(M)) + M) @ L.T for omega in omegas])
        
        return Ss

class Output:
    def __init__(self, system, inp):
        self.system = system
        self.input = inp
        
        
