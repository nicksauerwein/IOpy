# Input-output formalism
In this section, the theory behind the IOpy calculations is introduced.
<br />There are essentially two main approaches through modeling of open quantum systems. First is density matrix approach and using master equations and second is using the Langevin equations, which is also known as input-output theory. Input-output theory allows us to directly model the quatum fluctuations injected from any couplings port into the system. Quantum Langeving equations are formulated on the level of Heisenberg equations of motion describing the time evolution of any operator of the system. Moreover, in case of optical cavities any coherent laser drive that may be present can be taken into account. For more details see [Gardiner and Zoller (2004)](https://www.google.com) and [Clerk et al. (2010)](http://dx.doi.org/10.1103/RevModPhys.82.1155).

<br />For example for an optical cavity which is driven by a coherent laser field with the detuning $\Delta$ from the cavity resonance frequency, via a coupling of $\kappa_{ex}$ and is also coupled to the enviroment through the dissipation rate of $\kappa_0$ the equations of motion can be written as:

$$\dot a = -\frac{\kappa}{2}a + i\Delta a + \sqrt{\kappa_{ex}}a_{in} + \sqrt{\kappa_{0}}f_{in}$$

Where $\kappa = \kappa_0 + \kappa_{ex}$ is the total dissipation rate. $a_{in}$ and $f_{in}$ are field operators of the driving field and the stochastic thermal field respectively. This equation can also be written in terms of quadrature operators:

$$\dot X = \Delta Y -\frac{\kappa}{2}X + \sqrt{\kappa_{ex}}X_{in,ex} + \sqrt{\kappa_{0}}X_{in,0}$$
$$\dot Y = -\Delta X -\frac{\kappa}{2}Y + \sqrt{\kappa_{ex}}Y_{in,ex} + \sqrt{\kappa_{0}}Y_{in,0}$$

According to the input-output theory of open quantum systems the output field (which in case of optical cavity can be the reflected or transmitted light through the cavity) is given by:

$$a_{out} = a_{in} - \sqrt{\kappa_{ex}}a$$

Or in terms of quadratures:
$$X_{out,ex} = X_{in,ex} - \sqrt{\kappa_{ex}}X$$
$$Y_{out,ex} = Y_{in,ex} - \sqrt{\kappa_{ex}}Y$$


In general, any set of Langevin equations can in principle be linearized around the stationary solutions and can be written in a simillar way:

$$\dot Z = \textbf{M}Z + \textbf{L}Z_{in} \tag{1}$$

With the input-output relations:
$$Z_{out} = Z_{in} - \textbf{L}^TZ \tag{2}$$

Where $Z$ is a vertical vector containing the quadreture operators of different oscillatros involved in the dynamics and $Z_{in}$ and $Z_{out}$ are vectors containing the qudreture operatos of the input and output fields. For the optical cavity of the example above we have:

$$Z = \begin{pmatrix} X \\ Y \end{pmatrix},\quad Z_{in} = \begin{pmatrix} X_{in,ex} \\ Y_{in,ex} \\ X_{in,0} \\ Y_{in,0}\end{pmatrix},\quad Z_{out} = \begin{pmatrix} X_{out,ex} \\ Y_{out,ex} \\ X_{out,0} \\ Y_{out,0}\end{pmatrix} $$

And:

$$\textbf{M} = \begin{pmatrix} -\frac{\kappa}{2} &\Delta
                             \\-\Delta           &-\frac{\kappa}{2} \end{pmatrix}, \quad 
  \textbf{L}= \begin{pmatrix} \sqrt{\kappa_{ex}} &0 &\sqrt{\kappa_{0}} &0
                            \\0 &\sqrt{\kappa_{ex}} &0 &\sqrt{\kappa_{0}}\end{pmatrix}$$
<br />Due to the linearity of the equations one can take the Fourier transform of the equations and define a scattering matrix which relates the output fields to the input fields:

$$Z_{out}(\omega) = \textbf{S}(\omega)Z_{in}(\omega) \tag{3}$$

Where:

$$\textbf{S} = \mathbb{1} + \textbf{L}^T(i\omega+\textbf{M})^{-1}\textbf{L} \tag{4}$$



# Measurements
In IOpy calculations there are two ways to measure the output fields, which are essentially same as what we do in practice. First is the linear response of the system, which is simillar to output of a VNA. And second is the spectrum of the output field, which is the same as the ouput of the spectrum analyser.
## Linear response
According to the [Equation (3)](http://127.0.0.1:8000/theory/#input-output-formalism), a quadrature pair of any output port $i$ can be related to the quadrature pair of any input port $j$ using a submatrix of the scattering matrix:

$$\begin{pmatrix}X_{out,i} \\ Y_{out,i}\end{pmatrix} = \textbf{S}^{(ij)} \begin{pmatrix}X_{in,j} \\ Y_{in,j}\end{pmatrix} \tag{5}$$
Then the output field operator can be written as:
$$a_{out,i} = \frac{X_{out,i} + iY_{out,i}}{\sqrt2} = (\textbf{S}^{(ij)}_{11} + i\textbf{S}^{(ij)}_{21})\frac{X_{in,j}}{\sqrt2} +
                                       (\textbf{S}^{(ij)}_{22} - i\textbf{S}^{(ij)}_{12})\frac{iY_{in,j}}{\sqrt2}$$
In many cases the input field is a coherent drive with constant amplitude. Therefore, $X_{in,j}$ and In many cases the input field is a coherent drive with constant amplitude. Therefore, $X_{in,j}$ and 

$X_{in,j}$ and $Y_{in,j}$ are cosine part and sine part of the input field. In many cases the input field is a coherent drive with constant amplitude. Therefore, choosing any arbitrary values for the quadratures, as long as they satisfy the identity $X_{in,j}^2+Y_{in,j}^2=1$, will only impose a total phase shift to the response. By choosing $Y_{in,j}$ to be zero, we consider this phase shift to be zero and $a_{in,j}=X_{in,j}/\sqrt2$. as a result, any phase response in the output is being calculated with respect to the input field.

$$a_{out,i} = (\textbf{S}^{(ij)}_{11} + i\textbf{S}^{(ij)}_{21})a_{in,j}$$

or in a more familiar notation:
$$\chi^{(ij)}(\omega) = \textbf{S}^{(ij)}_{11} + i\textbf{S}^{(ij)}_{21}$$
## Spectra