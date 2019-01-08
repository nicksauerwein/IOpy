import numpy as np
from scipy.constants import epsilon_0, hbar, k

class MeasurementOperator:
    '''
    This class represents a general measurment with a measurement operator for defining a correlator.
    
    Q(t) = <Q_ij * Z_out,i(0) * Z_out,j(t)>
    
    Where Q_ij is the ij-th element of the measurement operator.
    '''
    def __init__(self, Q, system, omega_d = 0):

        self.system = system

        self.omega_d = omega_d

        self.Q = Q


class PowerMeasurement:
    '''
    A power measurement scheme object.
    The correlator function and measurement matrix in this scheme are:
    Q(t) = <q(0)q(t) + iq(0)p(t) - ip(0)q(t) + p(0)p(t)>
    [Q] = [ 1  i]
          [-i  1]
          
    Attributes:
        system: the system which the output field is coming from.
        omega_d: the driving frequency of the mode which the output field is coming from.
        Q: the measurment matrix.
    '''
    def __init__(self, output):
        '''
        Args:
            output: the output field we want to measure its spectrum.
        '''
        self.system = output.system

        self.omega_d = output.mode.omega_d

        r = np.argwhere(output.system.inputs == output.input)[0,0]

        n = len(output.system.inputs)

        self.Q = np.zeros((2*n,2*n), dtype = 'complex128')

        self.Q[2*r, 2*r] = 1
        self.Q[2*r, 2*r+1] = 1j

        self.Q[2*r + 1, 2*r + 1] = 1
        self.Q[2*r + 1, 2*r] = -1j

class HomodynMeasurement:
    '''
    A Homodyn measurement scheme object with a theta phase.
    The correlator function and measurement matrix in this scheme are:
    Q(t) = <cos^2(theta) q(0)q(t) + sin(theta)cos(theta) q(0)p(t) + sin(theta)cos(theta) p(0)q(t) + sin^2(theta) p(0)p(t)>
    [Q] = [cos^2(theta)         sin(theta)cos(theta)]
          [sin(theta)cos(theta)         sin^2(theta)]
    Attributes:
        system: the system which the output field is coming from.
        omega_d: the driving frequency of the mode which the output field is coming from.
        Q: the measurment matrix.
    '''
    def __init__(self, output, theta):
        '''
        Args:
            output: the output field we want to measure its spectrum.
            theta: the phase of the Homodyne measurement in radians.
        '''
        self.system = output.system

        self.omega_d = 0

        r = np.argwhere(output.system.inputs == output.input)[0,0]

        n = len(output.system.inputs)

        self.Q = np.zeros((2*n,2*n), dtype = 'complex128')

        self.Q[2*r, 2*r] = np.cos(theta)**2
        self.Q[2*r, 2*r+1] = np.cos(theta)*np.sin(theta)
        self.Q[2*r + 1, 2*r + 1] = np.sin(theta)**2
        self.Q[2*r+1, 2*r] = np.cos(theta)*np.sin(theta)


def linear_response(Omegas, system, output, Input, plot = False):
    '''
    The linear response (susceptibility) of the system from one specific input port to an output port in frequency domain:
    a_out = X * a_in
    
    Args:
        Omegas: the frequencies vector we want to claculate the linear response for them, in frame of the input field (not a 
                rotating frame)
        system: the system which we want to measure its response.
        output: the output port.
        Input: the input port.
        plot: flag, indicates to plot the susceptibilities or not.
        
    Returns:
        omegas_out: the frequencies vector we want to claculate the linear response for them, in frame of the output field (not a 
                rotating frame)
        chi: the susceptibility we want to measure.
    '''
    omega_d_in = Input.mode.omega_d
    omegas = Omegas - omega_d_in

    S = system.SMatrix(omegas)

    omega_d_out = output.mode.omega_d
    i = np.argwhere(system.inputs == Input)
    j = np.argwhere(system.inputs == output.input)

    omegas_out = omegas + omega_d_out
       
    chi = S[:,2*j,2*i] + 1j * S[:,2*j+1,2*i]
    if plot:
        from plots import plot_linear_response
        plot_linear_response(omegas_out, chi[:,0,0], system, output, Input)

    return omegas_out, chi[:,0,0]


def spectrum(omegas, measurement, components = False, plot = False):
    '''
    The spectrum of an output field.
    
    Args:
        omegas: the frequencies vector we want to claculate the spectrum for them, in frame of the output field (not a 
                rotating frame)
        measurement: the measurement scheme, of kinds PowerMeasurement or HomodynMeasurement.
        components: flag, indicates to calcuate different contributions of noise sources or just calculate the whole spectrum.
        plot: flag, indicates to plot the spectra or not.
        
    Returns:
        spec: the spectrum of the output field.
    '''
    omega_d = measurement.omega_d

    omegas_p = omegas
    omegas = omegas - omega_d
    system = measurement.system

    S1 = system.SMatrix(-omegas)
    S2 = np.conjugate(S1) #system.SMatrix(omega)

    ni = int(S1.shape[1]/2)

    lo = len(omegas)

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

            res += Q[i,j] * np.array([S1[:,i,k] * S2[:,j,k] * system.inputs[int(k/2)].spectrum(omegas) for k in range(2*ni)]).T

            #spec[i, j] += Q[i,j] * np.array([S1[i,k] * S2[j,k] * (system.inputs[int(k/2)].spectrum(omega) - 0.25) for k in range(2*ni)])
            #quantum term

            #specQ[i, j] = Q[i,j] * 1j/2 * np.sum([(S2[i,2*r] * S1[j,2*r+1] - S2[i,2*r + 1] * S1[j,2*r])  for r in range(ni)])

    #res = np.sum(np.sum(spec,axis = 0), axis = 0)

    #resQ = np.sum(np.sum(specQ))
    #res = np.append(res, resQ)


    if components:
        spec = np.real (np.cumsum(res, axis = -1))

    else:
        spec = np.real(np.sum(res, axis = -1)) #* hbar * (omega + output.input.omega_drive)

    if plot:
        from plots import plot_spectrum
        plot_spectrum(omegas_p, spec, components, system, )

    return spec
#spectrum = np.vectorize(spectrum)
