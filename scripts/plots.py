import numpy as np
from scipy.constants import epsilon_0, hbar, k
import matplotlib.pyplot as plt

def plot_linear_response(omegas, A, system, output, Input):
    '''
        This function is for plotting the linear response functions. It plots the absolute value and phase of the linear response 
        as well as plotting the linear response in complex space.
        
        Args:
            omegas: the vector containing the frequecnies in rad/sec (not in a rotating frame).
            A: the linear response function.
            system: the system which the linear response is from.
            output: the output field we that the linear response is calculated for.
            input: the input field we that the linear response is calculated for.
    '''
    omegas -= output.mode.omega_d
    Name = 'S_'+output.mode.name+Input.mode.name

    plt.figure()
    plt.plot(np.real(A), np.imag(A), label = 'linear response in quadreture space')
    ax = plt.gca()
    ax.set_aspect('equal')
    plt.xlabel('Real{' + Name + '}')
    plt.ylabel('Imag{' + Name + '}')
    plt.tight_layout()
    plt.grid()

    plt.figure()
    plt.plot((omegas + output.mode.omega_d)/2/np.pi, np.abs(A))
    plt.xlabel('Output Frequency [Hz]')
    plt.ylabel('|' + Name + '|')
    ax1 = plt.gca()
    ax1.set_xlim(min(omegas + output.mode.omega_d)/2/np.pi , max(omegas + output.mode.omega_d)/2/np.pi)
    plt.grid()
    ax2 = ax1.twiny()
    ax2.set_xlabel('Input Frequency [Hz]')
    plt.xticks(color='r', alpha = 0.6)
    ax2.set_xlim(min(omegas + Input.mode.omega_d)/2/np.pi , max(omegas + Input.mode.omega_d)/2/np.pi)
    plt.tight_layout()
    plt.grid(color='r', alpha = 0.3)

    plt.figure()
    plt.plot((omegas + output.mode.omega_d)/2/np.pi, np.angle(A))
    plt.xlabel('Output Frequency [Hz]')
    plt.ylabel('<' + Name)
    plt.yticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
    ax1 = plt.gca()
    ax1.set_xlim(min(omegas + output.mode.omega_d)/2/np.pi , max(omegas + output.mode.omega_d)/2/np.pi)
    plt.grid()
    ax2 = ax1.twiny()
    ax2.set_xlabel('Input Frequency [Hz]')
    plt.xticks(color='r', alpha = 0.6)
    ax2.set_xlim(min(omegas + Input.mode.omega_d)/2/np.pi , max(omegas + Input.mode.omega_d)/2/np.pi)
    plt.tight_layout()
    plt.grid(color='r', alpha = 0.3)


def plot_spectrum(omegas, spec, components, system):
    '''
        This function is for plotting the spectra.
        
        Args:
            omegas: the vector containing the frequecnies in rad/sec (not in a rotating frame).
            spec: the spectrum.
            componenets: flag, indicates to plot different contributions of noise sources in the spectrum or just plot the whole 
            spectrum.
            system: the system which the spectrum is from.
    '''
    if components:
        plt.figure()
        for i, inp in enumerate(system.inputs):
            plt.plot(omegas/2/np.pi, spec[:,2*i], label = str(inp) + ' Amp')
            plt.plot(omegas/2/np.pi, spec[:,2*i + 1], label = str(inp) + ' Phase')
            plt.xlabel('Frequency [Hz]')
            plt.ylabel(r'$S_{aa}/\hbar \omega$ [Hz$^{-1}$]')
        plt.gca().legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
            ncol= len(system.inputs))
        plt.tight_layout()
        plt.grid()

        """plt.figure()
        plt.xlabel('Frequency [Hz]')
        plt.ylabel(r'$S_{aa}/\hbar \omega$ [Hz$^{-1}$]')
        plt.plot(omegas/2/np.pi, spec[:,-1], label = 'Measureable Spectum');
        plt.gca().legend(loc='upper center', bbox_to_anchor=(0.5, 1.15))
        plt.tight_layout()
        plt.grid()""";

    else:
        plt.figure()
        plt.xlabel('Frequency [Hz]')
        plt.ylabel(r'$S_{aa}/\hbar \omega$ [Hz$^{-1}$]')
        plt.plot(omegas/2/np.pi, spec, label = 'Measureable Spectum');
        plt.gca().legend(loc='upper center', bbox_to_anchor=(0.5, 1.15))
        plt.tight_layout()
        plt.grid()
