# Input-Output Formalism
On this Page, the theory behind the IOpy calculations is introduced.

There are different approaches to model open quantum systems. But the two most commonly used ones are the density matrix approach using master equations and the Langevin equations, which is also known as input-output theory. Input-output theory allows us to directly model the quantum fluctuations injected from any port into the system. Quantum Langevin equations are formulated on the level of the Heisenberg equations of motion describing the time evolution of any operator of the system. Moreover, in case of optical cavities any coherent laser drive that may be present can be taken into account. For more details see [Gardiner and Zoller (2004)](https://www.springer.com/de/book/9783540223016) and [Clerk et al. (2010)](http://dx.doi.org/10.1103/RevModPhys.82.1155).

<br />For example, for an optical cavity which is driven by a coherent laser field with the detuning $\Delta$ from the cavity resonance frequency, via a coupling of $\kappa_{ex}$ and is also coupled to the environment through the dissipation rate of $\kappa_0$, the equations of motion can be written as

$$\dot a = -\frac{\kappa}{2}a + i\Delta a + \sqrt{\kappa_{\text{ex}}}a_{\text{in},\text{ex}} + \sqrt{\kappa_{0}}a_{\text{in},0},$$

where $\kappa = \kappa_0 + \kappa_{\text{ex}}$ is the total dissipation rate. $a_{\text{in},\text{ex}}$ and $a_{\text{in},0}$ are input operators of the driving field and the stochastic thermal field respectively. This equation can also be written in terms of quadrature operators

$$\dot X = \Delta Y -\frac{\kappa}{2} X + \sqrt{\kappa_{\text{ex}}}\, X_{\text{in},\text{ex}} + \sqrt{\kappa_{0}}\, X_{\text{in},0}$$
$$\dot Y = -\Delta X -\frac{\kappa}{2} Y + \sqrt{\kappa_{\text{ex}}}\, Y_{\text{in},\text{ex}} + \sqrt{\kappa_{0}}\, Y_{\text{in},0},$$

where the quadrature operators are defined as

$$X = \frac{a^\dagger + a}{\sqrt{2}},$$
$$Y = i\frac{a^\dagger - a}{\sqrt{2}}.$$

According to the input-output theory of open quantum systems, the output field (which in case of optical cavity can be the reflected or transmitted light through the cavity) is given by

$$a_{\text{out}} = a_{\text{in}} - \sqrt{\kappa_{\text{ex}}}a.$$

It can also be written in terms of quadratures
$$X_{\text{out},\text{ex}} = X_{\text{in},\text{ex}} - \sqrt{\kappa_{\text{ex}}}\, X,$$
$$Y_{\text{out},\text{ex}} = Y_{\text{in},\text{ex}} - \sqrt{\kappa_{\text{ex}}}\, Y.$$


Any set of Langevin equations, linearized around a stationary solution, can in principle be written in the form

$$\dot Z = \textbf{M}Z + \textbf{L}Z_{\text{in}} \tag{1},$$

with the input-output relations
$$Z_{\text{out}} = Z_{\text{in}} - \textbf{L}^TZ,$$

where $Z$ is a vector containing the quadrature operators of different oscillators involved in the dynamics. $Z_{\text{in}}$ and $Z_{\text{out}}$ are vectors containing the quadrature operators of the input and output fields. For the optical cavity of the example above we have

$$Z = \begin{pmatrix} X \\ Y \end{pmatrix},\quad Z_{\text{in}} = \begin{pmatrix} X_{\text{in},\text{ex}} \\ Y_{\text{in},\text{ex}} \\ X_{\text{in},0} \\ Y_{\text{in},0}\end{pmatrix},\quad Z_{\text{out}} = \begin{pmatrix} X_{\text{out},\text{ex}} \\ Y_{\text{out},\text{ex}} \\ X_{\text{out},0} \\ Y_{\text{out},0}\end{pmatrix}$$

and

$$\textbf{M} = \begin{pmatrix} -\frac{\kappa}{2} &\Delta
                             \\-\Delta           &-\frac{\kappa}{2} \end{pmatrix}, \quad 
  \textbf{L}= \begin{pmatrix} \sqrt{\kappa_{\text{ex}}} &0 &\sqrt{\kappa_{0}} &0
                            \\0 &\sqrt{\kappa_{\text{ex}}} &0 &\sqrt{\kappa_{0}}\end{pmatrix}.$$

Due to the linearity of the equations one can take the Fourier transform of the equations and define a scattering matrix which relates the output fields to the input fields

$$Z_{\text{out}}(\omega) = \textbf{S}(\omega)Z_{\text{in}}(\omega) \tag{2},$$

where

$$\textbf{S} = 1 + \textbf{L}^T(i\omega+\textbf{M})^{-1}\textbf{L} \tag{3}.$$



# Measurements
IOpy implements two different methods to characterize a linear system. They mimic closely the different types of measurements performed in the laboratory. First is the linear response of the system, which is similar to output of a vector network analyser (VNA). And, second is the spectrum of the output field, which is the same as the output of the spectrum analyser.

## Linear Response
According to the [Equation (2)](http://127.0.0.1:8000/theory/#input-output-formalism), a quadrature pair of any output port $i$ can be related to the quadrature pair of any input port $j$ using a submatrix of the scattering matrix

$$\begin{pmatrix}X_{\text{out},i} \\ Y_{\text{out},i}\end{pmatrix} = \textbf{S}^{(ij)} \begin{pmatrix}X_{\text{in},j} \\ Y_{\text{in},j}\end{pmatrix}.$$

Then the output field operator can be written as

$$a_{\text{out},i} = \frac{X_{\text{out},i} + iY_{\text{out},i}}{\sqrt2} = (\textbf{S}^{(ij)}_{11} + i\textbf{S}^{(ij)}_{21})\frac{X_{\text{in},j}}{\sqrt2} +
                                       (\textbf{S}^{(ij)}_{22} - i\textbf{S}^{(ij)}_{12})\frac{iY_{\text{in},j}}{\sqrt2}.$$


In many cases the input field is a coherent drive with constant amplitude and $X_{\text{in},j}$ and $Y_{\text{in},j}$ are cosine part and sine part of it. Therefore, choosing any arbitrary values for the quadratures, as long as they satisfy the identity $X_{\text{in},j}^2+Y_{\text{in},j}^2=1$, will only impose a total phase shift to the response. By choosing $Y_{\text{in},j}$ to be zero, we consider this phase shift to be zero and $a_{\text{in},j}=X_{\text{in},j}/\sqrt2$. as a result, any phase response in the output is being calculated with respect to the input field.

$$a_{\text{out},i} = (\textbf{S}^{(ij)}_{11} + i\textbf{S}^{(ij)}_{21})a_{\text{in},j}$$

or in a more familiar notation
$$\chi^{(ij)}(\omega) = \textbf{S}^{(ij)}_{11} + i\textbf{S}^{(ij)}_{21} \tag{4}.$$

## Spectra
In general for analyzing the spectrum of some measured signals, we can define a correlator using a measurement matrix $Q_{ij}$

$$Q(\tau) = \langle Q_{ij}Z_{\text{out},i}(0)Z_{\text{out},j}(\tau)\rangle,$$

where we have used the Einstein notation for the summations. The Fourier transform of this correlator would be the spectral density or spectrum

$$S_{QQ}[\omega] = \int_{-\infty}^{\infty} Q(\tau) e^{i\omega\tau}d\tau.$$

Due to the linearity of the expectation value and the integral, the spectrum can be rewritten in the following way

$$ S_{QQ}[\omega] = \frac{1}{2\pi} Q_{ij}\int_{-\infty}^{\infty} \langle Z_{\text{out},i}(\omega_1)Z_{\text{out},j}(\omega) \rangle d\omega_1.$$

According to [Equation (2)](http://127.0.0.1:8000/theory/#input-output-formalism), we can write the output signals in terms of input signals

$$Z_{\text{out},i}(\omega) = S_{ik}(\omega)Z_{\text{in},k}(\omega),$$
$$S_{QQ}[\omega] = \frac{1}{2\pi} Q_{ij}\int_{-\infty}^{\infty}S_{ik}(\omega_1)S_{jl}(\omega) \langle Z_{\text{in},k}(\omega_1)Z_{\text{in},l}(\omega) \rangle d\omega_1 \tag{5}.$$

In general, the input signals can be correlated with each other and have complicated statistical behaviors. In many situations (such as thermal input noises) it's a good approximation to consider different sources to be uncorrelated. More precisely

$$\langle Z_{\text{in},k}(\omega_1)Z_{\text{in},l}(\omega) \rangle = 2\pi\delta_{kl}\mathcal{S}_k^{\text{in}}(\omega)\delta(\omega_1+\omega),$$

where $\mathcal{S}_k^{\text{in}}(\omega)$ is the spectral density of the $k^\text{th}$ input signal. Now, we can simplify Equation (5) to

$$S_{QQ}[\omega] = Q_{ij}S_{ik}(-\omega)S_{jk}(\omega)\mathcal{S}_k^{\text{in}}(\omega). $$

This final result is used in the calculations of IOpy. Here we make a remark on the summations by rearranging the terms in the following way

$$S_{QQ}[\omega] = \sum_k \mathcal{S}_k^{\text{in}}(\omega) (\sum_{i,j} Q_{ij}S_{ik}(-\omega)S_{jk}(\omega)) = \sum_k c_k(\omega)\mathcal{S}_k^{\text{in}}(\omega).$$

This illustrates that the spectrum can be expressed as a sum of the different input noise contributions.