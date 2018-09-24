import numpy as np
from scipy.constants import epsilon_0, hbar, k
import matplotlib.pyplot as plt

def plot_linear_response(omegas, A, system, output, input):
    omegas -= output.mode.omega_d
    plt.figure()
    plt.plot(np.real(A), np.imag(A), label = 'linear response in quadreture space')
    ax = plt.gca()
    ax.set_aspect('equal')
    plt.xlabel(r'$Real\{S_{aa}/\hbar \omega\}$')
    plt.ylabel(r'$Imag\{S_{aa}/\hbar \omega\}$')
    plt.tight_layout()
    plt.grid()

    plt.figure()
    plt.plot((omegas + output.mode.omega_d)/2/np.pi, np.abs(A))
    plt.xlabel('Output Frequency [Hz]')
    plt.ylabel(r'$|S_{aa}|/\hbar \omega$ [Hz$^{-1}$]')
    ax1 = plt.gca()
    ax1.set_xlim(min(omegas + output.mode.omega_d)/2/np.pi , max(omegas + output.mode.omega_d)/2/np.pi)
    ax2 = ax1.twiny()
    ax2.set_xlabel('Input Frequency [Hz]')
    ax2.set_xlim(min(omegas + input.mode.omega_d)/2/np.pi , max(omegas + input.mode.omega_d)/2/np.pi)
    plt.tight_layout()
    plt.grid()

    plt.figure()
    plt.plot((omegas + output.mode.omega_d)/2/np.pi, np.angle(A))
    plt.xlabel('Output Frequency [Hz]')
    plt.ylabel(r'$ < S_{aa}/\hbar \omega$')
    plt.yticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
    ax1 = plt.gca()
    ax1.set_xlim(min(omegas + output.mode.omega_d)/2/np.pi , max(omegas + output.mode.omega_d)/2/np.pi)
    ax2 = ax1.twiny()
    ax2.set_xlabel('Input Frequency [Hz]')
    ax2.set_xlim(min(omegas + input.mode.omega_d)/2/np.pi , max(omegas + input.mode.omega_d)/2/np.pi)
    plt.tight_layout()
    plt.grid()
