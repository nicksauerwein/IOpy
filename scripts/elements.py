import numpy as np
from scipy.constants import epsilon_0, hbar, k

class Mode:
    '''
    Harmonic oscillators of any kind can be defined using this class.
    Attributes:
        name: name of the mode.
        omega: resonance frequency of the mode in rad/sec.
        kappa: mode total dissipation rate in rad/sec.
        omega_rot: frequency at which the mode frame is rotating in rad/sec.
        driven: flag indicates whether the mode is driven or not.
    '''
    def __init__(self,name, omega):
        '''
        Args:
            name: a string containing name of the mode.
            omega: resonance frequency of the mode in rad/sec.
        '''
        self.name = name
        self.omega = omega      # resonance frequency of the mode
        self.omega_rot = omega  # frequency at which the mode frame is rotating
        self.kappa = 0          # mode total dissipation rate

        self.driven = False     # flag indicates whether the mode is driven or not

    @property
    def omega_d(self):
        '''
        returns the frequency of the field which is driving the mode
        '''
        return self.omega - self.omega_rot

    def __str__(self):

        return self.name

class Input:
    '''
    Input field coupled to a mode. Inputs can be coherent drives (pumps) or thermal baths.
    Attributes:
        name: name of the input field.
        mode: the mode which the input is coupled to.
        kind: flag which indicates the input is a pump or a thermal bath. 'drive' for a pump and 'bath' for a thermal bath.
        kappa: coupling rate to the mode in rad/sec..
        omega_drive: frequency of the pump fields in rad/sec.
        bath_temp: tempreture of the bath or the pump in Kelvins.
        nbar: average number of thermal photons in the input field.
    '''
    def __init__(self,name, mode, kappa, kind = 'bath', omega_drive = 0, bath_temp = 0):
        '''
        Args:
            name: name of the input field.
            mode: the mode which the input is coupled to.
            kind: flag which indicates the input is a pump or a thermal bath. 'drive' for a pump and 'bath' for a thermal bath.
            kappa: coupling rate to the mode in rad/sec.
            omega_drive: frequency of the pump fields in rad/sec.
            bath_temp: tempreture of the bath or the pump in Kelvins. 
        
        Raises:
            ValueError: defining a second pump for a mode. 
        '''
        self.name = name
        self.mode = mode        # the mode which the input is coupled to
        self.kind = kind        # a coherent dirve (pump) or a thermal bath
        self.kappa = kappa      # coupling rate to the mode

        self.mode.kappa += kappa # the total dissipation rate of the mode has to be added by the coupling rate value

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

    def spectrum(self, omegas):
        '''
        spectrum of the input field. Here we approximatley take the thermal spectrum to be flat near the mode frequency.
        Args:
            omegas: the frequencies vector at which we want to calculate the spectrum.

        Returns:
            spectrum of the input field in units of number of photons.
        '''
        return 0.5 * self.nbar + 0.25 * np.ones_like(omegas)

    def __str__(self):

        return str(self.mode)+'_in,'+self.name



class Coupling:
    '''
    Couplings between two 'Mode's using the coupling vector.
    
    vg: coupling vector [real]

        H_int = 4 hbar ( vg[0] q1 q2 + vg[1] q1 p2 + vg[2] p1 q2 + vg[3] p1 p2)

        EXAMPLE
        For optomechanics:
        vg = [g , 0, 0, 0]
    
    Attributes:
        mode1: first mode.
        mode2: second mode.
        vg: coupling vector. a 4-d real vector.
    '''
    def __init__(self,mode1, mode2, vg):
        '''
        Args:
            mode1: first mode.
            mode2: second mode.
            vg: coupling vector. a 4-d real vector.
        '''
        self.mode1 = mode1
        self.mode2 = mode2

        self.vg = vg

    def __str__(self):

        return 'g_'+str(mode1)+str(mode2)



    def contains_mode(self,mode):
        '''
        indicates if the mode is involved in this coupling or not.
        
        Args:
            mode: the mode we want to look for.
        
        Returns:
            'True' if the mode is involved and 'False' for other wise.
        '''
        if mode1 == mode:
            True
        if mode2 == mode:
            True

        return False



class System:
    '''
    Defines the complex system made of coupled modes and inputs. It's most important purpose of it is for calculating the scattering matrix.
    
    Attributes:
        modes: an array of modes in the system.
        inputs: an array of inputs of the system.
        couplings: couplings between the modes of the system.
        M: the M matrix in the relation dZ/dt = M*Z + L*Z_in.
        L: the L matrix in the relation dZ/dt = M*Z + L*Z_in.
    '''
    def __init__ (self, modes = [], inputs = [], couplings = []):
        '''
        Arga:
            modes: an array of modes in the system.
            inputs: an array of inputs of the system.
            couplings: couplings between the modes of the system.
            M: the M matrix in the relation dZ/dt = M*Z + L*Z_in.
            L: the L matrix in the relation dZ/dt = M*Z + L*Z_in.
        '''
        self.modes = np.array(modes)
        self.inputs = np.array(inputs)
        self.couplings = np.array(couplings)

        self.make_ML()

    def add_mode(self,mode):
        '''
        Adding a mode to the system.
        
        Args:
            mode: the mode we want to add.
        '''
        np.append(self.modes ,mode)
        self.make_ML()

    def add_input(self,inp):
        '''
        Adding an input to the system.
        
        Args:
            inp: the input we want to add.
        '''
        np.append(self.inputs ,inp)
        self.make_ML()

    def add_coupling(self,coup):
        '''
        Adding a coupling to the system.
        
        Args:
            coup: the coupling we want to add.
        '''
        np.append(self.couplings ,coup)
        self.make_ML()

    def make_ML(self):
        '''
        Constructing M and L matrices of the system.
        '''
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
        '''
        Constructing the scattering matrix of the system for a frequency range.
    
        Args:
            omegas: frequencies vector in rad/sec.
            
        Returns:
            Ss: the scattering matrix.
        '''
        M = self.M
        L = self.L

        #lo = len(omegas)

        Ss = np.array([np.eye(len(L)) + L @ np.linalg.inv(1j * omega * np.eye(len(M)) + M) @ L.T for omega in omegas])

        return Ss

class Output:
    '''
    The output field of the system with respect to an input field (in terms of input-output formalism). 
    
    Attributes:
        system: the complex system of coupled modes and inputs.
        input: the input field which we want to define its output field (in terms of input-output formalism).
        mode: the mode which these input and output fields are coupled.
    '''
    def __init__(self, system, inp):
        '''
        Args:
            system: the complex system of coupled modes and inputs.
            inp: the input field which we want to define its output field (in terms of input-output formalism).
        '''
        self.system = system
        self.input = inp
        self.mode = inp.mode
