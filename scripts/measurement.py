import numpy as np
from scipy.constants import epsilon_0, hbar, k

class MeasurementOperator:

    def __init__(self, Q, system, omega_d = 0):

        self.system = system

        self.omega_d = omega_d

        self.Q = Q


class PowerMeasurement:

    def __init__(self, output):

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

    def __init__(self, output, theta):

        self.system = output.system

        self.omega_d = 0

        r = np.argwhere(output.system.inputs == output.input)[0,0]

        n = len(output.system.inputs)

        self.Q = np.zeros((2*n,2*n), dtype = 'complex128')

        self.Q[2*r, 2*r] = np.cos(theta)**2
        self.Q[2*r, 2*r+1] = np.cos(theta)*np.sin(theta)
        self.Q[2*r + 1, 2*r + 1] = np.sin(theta)**2
        self.Q[2*r+1, 2*r] = np.cos(theta)*np.sin(theta)


def linear_response(omegas, system, output, input, plot = False):
    omega_d_in = input.mode.omega_d

    omegas -= omega_d_in

    S = system.SMatrix(omegas)

    omega_d_out = output.mode.omega_d
    i = np.argwhere(system.modes == input.mode)
    j = np.argwhere(system.modes == output.mode)

    omegas_out = omegas + omega_d_out

    a = S[:,2*j,2*i] + 1j * S[:,2*j+1,2*i]

    if plot:
        from plots import plot_linear_response
        plot_linear_response(omegas_out, a[:,0,0], system, output, input)

    return omegas_out, a[:,0,0]


def spectrum(omegas, measurement, components = False, plot = False):

    omega_d = measurement.omega_d


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
        plot_spectrum(omegas, spec, components, system, )

    return spec
#spectrum = np.vectorize(spectrum)
