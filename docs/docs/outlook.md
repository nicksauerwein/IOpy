# Multimode optomechanics
One of the biggest motivations for starting the IOpy project was to develope a computational tool to help the experts in the field with the theoretical calculations. When the optomechanical systems become more complex the calculations also get more complicated and even impossible to do by hand without approximations. Especially, when the system invloves more oscillating modes like optical cavities, mechanical oscillators or driving fields. Multimode optomechanics, a growing field of interest, can be improved if such computational tools has the power to do the multimode calculations with an acceptable accuracy. But the barrier for the IOpy to do these calculations is arising from almost the same issue as when we want to drive an optical mode with more than one pump.

## Multidrive Issue
In many experiments in optomechanics we need to drive optical resonators with more than one pump field (for example see [Suh et. al. 2014](http://science.sciencemag.org/content/344/6189/1262)). In this case the theoretical calculations are not as clear as the simple case where each optical mode is driven by a single pump. The complexity is arising from the fact that due to the nonlinear nature of the optomechanical interaction, there would always be frequency mixing terms in the dynamics. In case of a single pump these mixings can be divided into fast and slowly varying terms and by going to the rotating frame of the drive, the equations of motions for the slowly varying terms become time independent and with linearizing the equations in principle they can be solved exactly in the frequency domain. But in case of multiple drives, because of the presence of multiple powerful tones, in general it is impossible to apply the same idea and equations of motion can not become time independent. In another language, there no longer exists a single rotating frame in which every other time variation can be considered slowly varying. The idea of having different rotating frames also fails because of the nonlinearities that prevents two rotating frames to be independent of each other.

However, there are some approaches to resolve the problem still in frequency domain. For example, in the case of driving a mode with two pumps one solution is to use the Floquet ansatz to expand the variables by a Fourier series with principle frequency equal to difference frequency of the two drives (see [Malz and Nunnenkamp, 2016](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.94.023803)). As another example, in the context of a four-mode isolator, where again each optical cavity is pumped with two drives to couple to two different mechanical modes simultaneously, the idea is to define the higher order mixing terms as "auxiliary modes" and expand the model to a model with higher number of modes as shown in the picture below from the work of [Peterson et. al., 2018](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.7.031001).

<!--
![The idea of the expanded mode basis for the four-mode isolator (Peterson et. al., 2018).](auxmodes.png){width=400 .center}
-->



<p align="center">
  <img width="460" src="https://github.com/nicksauerwein/IOpy/blob/master/docs/docs/auxmodes.png?raw=true">
    <p align = "center">
        The idea of the expanded mode basis for the four-mode isolator (Peterson et. al., 2018).
    </p>
</p>


But in both cases, the calculations rely on truncating an infinite series and using the approximations like rotating wave approximation which we want to avoid in IOpy for keeping the calculations general. Moreover, these ideas will result into huge complexity in case of more than two drives.

## Time Domain Simulations
These issues lead us to think about a totally different approach for the calculations which is adopted from what is really happening in the experiments. In experiments, a VNA measures the scattering matrix of a network injecting a coherent signal (a sine wave) to the network and extracting the amplitude and phase from the output of the network. This, we can exactly done with time-domain simulations. In principle, we can write the most general Hamiltonian of the optomechanical network as the following

$$H_{\text{sys}} = \sum_k \hbar\omega_{\text{cav},k}a^{\dagger}_ka_k + \sum_j \hbar\Omega_jb^{\dagger}_jb_j -\hbar\sum_{j,k,l}[g_0]_{kl}^ja^\dagger_ka_l(b^\dagger_j+b_j),$$

and

$$H_{\text{drive}} = \sum_{j,m}i\hbar\sqrt{\kappa_{jm}}(s_{\text{in},jm}(t)a^\dagger_je^{-i\omega_mt} + H.c.).$$

With this, we can derive the equations of motion in the time domain and we can define the output ports with the input-output theory as $s_{\text{out},jm} = s_{\text{in},jm} - \sqrt{\kappa_{jm}}a_j$. Then for calculating the scattering matrix we can simulate the equations of motion in the time domain for inputs as sine waves, spanning a frequency band. Then look at the Fourier transform of the output wave at the frequencies we are interested to extract the amplitude and phase of the response. Please note this scattering matrix will not be a simple scattering matrix anymore. Because for example for a single weak sine wave there can be multiple sine waves at the output but we can still look for the frequencies of interest. Once the scattering matrix is calculated, every other parameter like the spectrum can be calculated.

This simulation is done for a simple case of a single cavity. <!--To see the full code go to [TimeDomain - SimpleCavity](http://localhost:8888/notebooks/IOpy/iopy/Time%20Domain/TimeDomain%20-%20SimpleCavity.ipynb). -->The results for this simulation are shown in the figures below.

<!--
![The amplitude of the linear response calculated with time domain simulation](time/amp.png){width=460 .center}
\begin{figure}[!h]
\caption{The amplitude of the linear response calculated with time domain simulation}
\end{figure}

![The phase of the linear response calculated with time domain simulation](time/phase.png){width=460 .center}
\begin{figure}[!h]
\caption{The amplitude of the linear response calculated with time domain simulation}
\end{figure}
-->


<p align="center">
  <img width="460" src="https://github.com/nicksauerwein/IOpy/blob/master/docs/docs/time/amp.png?raw=true">
    <p align = "center">
        The amplitude of the linear response calculated with time domain simulation
    </p>
</p>

<p align="center">
  <img width="460" src="https://github.com/nicksauerwein/IOpy/blob/master/docs/docs/time/phase.png?raw=true">
    <p align = "center">
        The phase of the linear response calculated with time domain simulation
    </p>
</p>


Although this idea works for the simple cavity, we have to further develop the code in order to cope with more complex systems like the basic optomechanics. Developing a time domian calculation library for the IOpy is one of the main goals of the future.

# Beyond Optomechanics

Another future goal for IOpy is to use it for physical systems other than optomechanics. In IOpy calculations, the physical nature of the problem is not really taken into account. For example all the examples given so far are in microwave domain (for superconducting circuit optomechanics) but all of them can also be implemented for the optical domain. In principle, we can go even further. As it can be inferred from the package name (IO in IOpy stands for Input-Output) our goal is to develope IOpy in a way that it is able to simulate most phenomenon which deal with coupled oscillators that can be formulated in input-output formalism.
