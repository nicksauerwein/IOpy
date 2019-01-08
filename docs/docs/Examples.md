In this section a set of famous phenomena in optomechanics is presented. These calculations serve first as examples of using IOpy in simulating Langevin equations, and second are benchmarks of IOpy which can be compared to the known theoretical models.

# Simple Cavity 

<p align="center">
  <img width="260" src="\LC.png">
    <p align = "center">
        False-colour optical micrograph of the microwave resonator formed by a spiral inductor shunted by a parallel-plate capacitor (Teufel, Li et al., 2011)
    </p>
</p>


The first example is simulating a hot microwave resonator. Here the temperature of the bath is higher than the temperature of the drive and therefore we would expect to see an emmition shaped like a Lorenzian. To see the fool written example, go to [Simple cavity example](http://localhost:8888/notebooks/IOpy/iopy/examples/Simple%20Cavity.ipynb).

First we have to define the cavity mode:
```python
omega_c = 5e9*np.pi*2
a = Mode('a', omega_c)
```
Then we have to define input fields. In this example the cavity is driven by a coherent drive and is coupled to a thermal bath.
```python
kappa_ex = 0.2e6*np.pi*2
kappa_0 = 0.3e6*np.pi*2
kappa = kappa_ex + kappa_0

T_drive = 2e-5
T_bath = 10e-3

a_inex = Input('ex', a, kappa_ex, kind = 'drive',
                omega_drive = omega_c, bath_temp=T_drive)
a_in0 = Input('0', a, kappa_0, kind = 'bath', bath_temp=T_bath)
```
And finally the system object and the output field.
```python
sys_cav = System([a], [a_in0,  a_inex], [])
```
```python
a_outex = Output(sys_cav, a_inex)
```
Now for measuring the spectrum of the output field, we have to use the `spectrum` function:
```python
omegas = np.linspace(omega_c - 15*kappa, omega_c + 15*kappa, 1001)
spec = me.spectrum(omegas, me.PowerMeasurement(a_outex),
                   components = False, plot = True)
```
<!--
![Simple Cavity Spectrum](Simple Cavity/simple_cavity_spectrum.png){width=460 .center}
\begin{figure}[!h]
\caption{Simple cavity output spectrum}
\end{figure}
-->


<p align="center">
  <img width="460" src="\Simple Cavity\simple_cavity_spectrum.png">
    <p align = "center">
        cavity output spectrum
    </p>
</p>


As we expect, we can see a Lorentzian in the spectrum. If the tempreture of the driving field was higher than the thermal bath, we would see a deep instead of a peak.

The linear response of the system to driving can also be measured with the `linear_response` function:
```python
omegas_newex, S_ex = me.linear_response(omegas, sys_cav, a_outex, a_inex, plot = 1)
```
<!--
![cavity linear response in complex space](Simple Cavity/linear_response_comp.png){width=460 .center}
\begin{figure}[!h]
\caption{cavity linear response in complex space}
\end{figure}

![cavity linear response amplitude](Simple Cavity/linear_response_amp.png){width=460 .center}
\begin{figure}[!h]
\caption{cavity linear response amplitude}
\end{figure}

![cavity linear response phase](Simple Cavity/linear_response_phase.png){width=460 .center}
\begin{figure}[!h]
\caption{cavity linear response phase}
\end{figure}
-->

<p align="center">
  <img width="460" src="\Simple Cavity\linear_response_comp.png">
    <p align = "center">
        cavity linear response in complex space
    </p>
</p>

<p align="center">
  <img width="460" src="\Simple Cavity\linear_response_amp.png">
  <p align = "center">
        cavity linear response amplitude
  </p>
</p>
<p align="center">
  <img width="460" src="\Simple Cavity\linear_response_phase.png">
  <p align = "center">
        cavity linear response phase
  </p>
</p>


The results can also be compared to the theory. For example in this case the linear response of the system to the drive field is

$$ S_{aa} = 1 - \frac{\kappa_{ex}}{\frac{\kappa}{2} - i(\omega-\omega_c)}.$$

The graphs below show the comparison between this equation and IOpy results.

<!--
![cavity linear response amplitude](Simple Cavity/comparison_amp.png){width=460 .center}
\begin{figure}[!h]
\caption{cavity linear response amplitude}
\end{figure}

![cavity linear response phase](Simple Cavity/comparison_phase.png){width=460 .center}
\begin{figure}[!h]
\caption{cavity linear response phase}
\end{figure}
-->

<p align="center">
  <img width="460" src="\Simple Cavity\comparison_amp.png">
  <p align = "center">
        cavity linear response amplitude
  </p>
</p>
<p align="center">
  <img width="460" src="\Simple Cavity\comparison_phase.png">
  <p align = "center">
        cavity linear response phase
  </p>
</p>



# Basic optomechanics and cooling
<p align="center">
  <img width="260" src="\drum.png">
    <p align = "center">
        False-colour scanning electron micrograph showing the upper plate of the capacitor suspended ,50 nm above the lower plate and free to vibrate like a taut, circular drum.  (Teufel, Li et al., 2011)
    </p>
</p>

          
In this example we simulate an optomechanical system with a weak drive. Here we want to see the optomechanical cooling due to the increase in optomechanical damping rate. To see the fool written example, go to [Basic optomechanics](http://localhost:8888/notebooks/IOpy/iopy/examples/Basic%20Optomechanics.ipynb).

In the basic optomechanical interaction, the cavity resonance frequency shifts by a constant value due to the DC nonlinearity. Therefore, before difining the modes we have to calculate this DC shift.

```python
omega_c = 5e9*np.pi*2     # cavity resonance frequency

kappa_0 = 0.3e6*np.pi*2
kappa_ex = 0.4e6*np.pi*2

kappa = kappa_0 + kappa_ex

omega_m = 5e6*np.pi*2    # mechanical resonance frequency
gamma_m = 100*np.pi*2

P_in = 5e-12

g_0 = 200*np.pi*2

omega_drive = omega_c - 1* omega_m


from DCnonlinearities import optomechanics

omdir = optomechanics(P_in, kappa_0, kappa_ex, omega_c,
                      omega_drive, omega_m, g_0)

g= omdir['g']  # optomechanical coupling rate = sqrt(nbar)*g_0
omega_c = omdir['omega_c']   # new cavity resonance frequency
```
Now we can define the modes, as well as input fields including thermal baths coupled to optics and mechanics and the optical driving field.

```python
a = Mode('a', omega_c)
b = Mode('b', omega_m)

a_inex = Input('ex', a, kappa_ex, kind = 'drive',
                omega_drive = omega_drive, bath_temp=10e-3)
a_in0 = Input('0', a, kappa_0, kind = 'bath', bath_temp=10e-3)

b_in0 = Input('0', b, gamma_m, kind = 'bath', bath_temp=10e-3)
```

Then we should define the coupling between the optical and mechanical modes:

```python
g_ab = Coupling(a, b, g * np.array([1,0,0,0]))
```
And finally the whole optomechanical system:

```python
sys_om = System([a, b], [a_in0,b_in0 , a_inex], [g_ab])
```

Now just like the previous example we can measure the spectrum of the output field.
<!--
![optomechanical cavity output spectrum](Basic OM/spec.png){width=460 .center}
\begin{figure}[!h]
\caption{optomechanical cavity output spectrum}
\end{figure}
-->

<p align="center">
  <img width="460" src="\Basic OM\spec.png">
    <p align = "center">
        optomechanical cavity output spectrum
    </p>
</p>

The peak that can be seen is because of low sampling rate of the calculations. To have a better precission we zoom on the neighbourhood of the cavity resonance frequency.

<!--
![optomechanical cavity output spectrum](Basic OM/spec_zoom.png){width=460 .center}
\begin{figure}[!h]
\caption{optomechanical cavity output spectrum}
\end{figure}
-->

<p align="center">
  <img width="460" src="\Basic OM\spec_zoom.png">
    <p align = "center">
        optomechanical cavity output spectrum
    </p>
</p>


Here we can clearly see different contribuitions to the spectrum. In addition the width of the spectrum is equal to the theory value $\Gamma_{eff} = \Gamma_m (1 + C)$ (with $C$ as the cooperativity equal to $\frac{4g^2}{\kappa\Gamma_m}$) which results in cooling.


# Strong coupling regime
<p align="center">
  <img width="260" src="\Strong.png">
    <p align = "center">
        Mechanical frequency spectrum (fre- quency on vertical axis) as a function of laser detuning, for a strongly coupled optomechanical system. (Aspelmeyer, Kippenberg, Marquardt 2014)
    </p>
</p>


In this example we show the effect of increasing of the laser input power ($P_{in}$). For the details on the theory see [(Aspelmeyer, Kippenberg, Marquardt (2014))](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.86.1391), section VII.C. By increasing the input power, at the beginning we will only see an imporevement in the cooling, but as we continue with increasing the power the optical and mechanical modes hybridize to form two new modes with the eigenfrequencies

$$ \omega_{\pm} = \frac{\Omega_m-\Delta}{2} \pm \sqrt{g^2 + (\frac{\Omega_m+\Delta}{2})^2}.$$

When the driving laser is exactly detuned on the red sideband ($\Delta=-\Omega_m$) the splitting of these two modes is equal to $2g$. In this example we want to show this splitting on the spectrum.

To this end, the code is exactly the same as the previous example but with a different input power. To see the full code go to [Strong coupling regime](http://localhost:8888/notebooks/IOpy/iopy/examples/Strong%20Coupling%20Regime.ipynb). 
```python
P_in = 5e-9
```
By measuring the output filed spectrum we can clearly see this mode splitting:

<!--
![optomechanical cavity output spectrum](Strong coupling/spec0.png){width=460 .center}
\begin{figure}[!h]
\caption{optomechanical cavity output spectrum}
\end{figure}
-->

<p align="center">
  <img width="460" src="\Strong coupling\spec0.png">
    <p align = "center">
        optomechanical cavity output spectrum
    </p>
</p>


To see better the splitting we change the measurement frequencies:

<!--
![optomechanical cavity output spectrum](Strong coupling/spec.png){width=460 .center}
\begin{figure}[!h]
\caption{optomechanical cavity output spectrum}
\end{figure}
-->

<p align="center">
  <img width="460" src="\Strong coupling\spec.png">
    <p align = "center">
        optomechanical cavity output spectrum
    </p>
</p>


# Optomechanically induced transparency
<p align="center">
  <img width="260" src="\omit.png">
    <p align = "center">
        Transmission of the probe laser power through the optomechanical system in the case of a critically coupled cavity k0 = kex as a function of normalized probe laser frequency offset, when the control field is off (blue lines) and on (green lines) (Weis et al., 2010).
    </p>
</p>
This is example is about the optomechanically induced transparency also known as OMIT. This effect was observed in atoms (electromagnetically induced transparency [Fleischhauer, Imamoglu, and Marangos, 2005](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.77.633)) as the cancellation of absorbtion in the presence of an auxiliary laser field. OMIT was predicted theoritcally by Schliesser, 2009 and [Agarwal and Huang 2010](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.81.041803). When the optical cavity is pumped on the red sideband, if we inject a weak probe field into the cavity the optomechanical interaction causes the cavity to be seen transparent by this weak field.

To simulate this phenomenan in IOpy, the setup is again simillar to the Basic optomechanics example. The difference here is that we set the driving field (control field, in this context) to be a high tempreture source. In this way, the noise around this control field play the roll of the weak probe field for us, so we can see the OMIT effect in the spectrum, as well as the linear response. To see the full code go to [OMIT](http://localhost:8888/notebooks/IOpy/iopy/examples/OMIT.ipynb) example.

```python
T_cont = 1
T_bath = 10e-3

a_cont = Input('ex', a, kappa_ex, kind = 'drive',
               omega_drive = omega_cont, bath_temp = T_cont)
a_in0 = Input('0', a, kappa_0, kind = 'bath', bath_temp = T_bath)

b_in0 = Input('0', b, gamma_m, kind = 'bath', bath_temp = T_bath)
```

And now we measure the spectrum and the linear response.

<!--
![optomechanical cavity output spectrum](omit/spec.png){width=460 .center}
\begin{figure}[!h]
\caption{optomechanical cavity output spectrum}
\end{figure}

![cavity linear response amplitude](omit/LR_amp.png){width=460 .center}
\begin{figure}[!h]
\caption{cavity linear response amplitude}
\end{figure}

![cavity linear response phase](omit/LR_phase.png){width=460 .center}
\begin{figure}[!h]
\caption{cavity linear response phase}
\end{figure}
-->


<p align="center">
  <img width="460" src="\omit\spec.png">
    <p align = "center">
        optomechanical cavity output spectrum
    </p>
</p>

<p align="center">
  <img width="460" src="\omit\LR_amp.png">
  <p align = "center">
        cavity linear response amplitude
  </p>
</p>

<p align="center">
  <img width="460" src="\omit\LR_phase.png">
  <p align = "center">
        cavity linear response phase
  </p>
</p>


These results can also be compared to theory. To see the details go to [OMIT Test](http://localhost:8888/notebooks/IOpy/iopy/Tests/OMIT%20Test.ipynb) notebook. By a calculation we can show for the transmission window:


$$T = 1 - \kappa_{ext}\frac{\chi_{opt}(\Omega)}{1 + g^2\chi_{omech}(\Omega)\chi_{opt}(\Omega)}$$
Where:
\begin{align}
    \chi_{opt}(\Omega) &= [-i(\Omega+\Delta)+\kappa/2]^{-1}\\
    \chi_{mech}(\Omega) &= [-i(\Omega-\Omega_m)+\Gamma_m/2]^{-1}
\end{align}
With:
$$\Delta = \omega_{cont} - \omega_{cav},\quad \Omega = \omega_p - \omega_{cont}$$

And the linear response from IOpy can be compared with this results:

<!--
![cavity linear response amplitude](omit/test_amp.png){width=460 .center}
\begin{figure}[!h]
\caption{cavity linear response amplitude}
\end{figure}

![cavity linear response phase](omit/test_phase.png){width=460 .center}
\begin{figure}[!h]
\caption{cavity linear response phase}
\end{figure}
-->


<p align="center">
  <img width="460" src="\omit\test_amp.png">
  <p align = "center">
        cavity linear response amplitude
  </p>
</p>

<p align="center">
  <img width="460" src="\omit\test_phase.png">
  <p align = "center">
        cavity linear response phase
  </p>
</p>


# Frequency conversion using OMIT
<p align="center">
  <img width="210" src="\conv.png">
    <p align = "center">
        Reciprocal mechanically-mediated frequency conversion (adapted from Peterson et. al. 2018).
    </p>
</p>
The last example is about the Frequency Conversion using OMIT effect, which is a step through multimode calculations. In this scenario, two optical modes with different resonance frequencies are two the same mechanical mode and the optical modes are pumped on their red sidebands. If we inject a weak probe to one of the cavities, when this probe is around resonance with this cavity there will be an emission from the other cavity, around its resonance frequency. The qualitative explanation is that when probe field is on resonance with the first cavity, it will beat with the pump and excite the mechanics. Then on the other cavitu beatting of the mechanics and the pump will excite a field which it's frequency is spaced from the second pump by the value of the mechanical resonance frequencies. These excitations are both at red and blue sides of the pump, which the blue side would be the resonance frequency of the second cavity.

To see this effect in IOpy first we have to define the whole system as two optical modes each with one drive, tuned on their red sidebands and coupled to a shared mechanical mode. To see the full code, go to [Frequency Conversion using OMIT](http://localhost:8888/notebooks/IOpy/iopy/examples/Frequency%20Conversion%20using%20OMIT.ipynb).
```python
omega_cav1 = 5e9*np.pi*2
kappa_01 = 0.3e6*np.pi*2
kappa_ex1 = 0.4e6*np.pi*2

omega_cav2 = 6e9*np.pi*2
kappa_02 = 0.3e6*np.pi*2
kappa_ex2 = 0.4e6*np.pi*2


omega_m = 5e6*np.pi*2
gamma_m = 100*np.pi*2

g_01 = 200*np.pi*2
g_02= 200*np.pi*2


P_in1 = 8e-10
Delta1 = -omega_m
omega_cont1 = omega_cav1 + Delta1
T_cont1 = 2
bath_temp1 = 10e-3

P_in2 = 8e-10
Delta2 = -omega_m
omega_cont2 = omega_cav2 + Delta2
T_cont2 = 2
bath_temp2 = 10e-3

from DCnonlinearities import optomechanics

omdir1 = optomechanics(P_in1, kappa_01, kappa_ex1,
                       omega_cav1, omega_cont1, omega_m, g_01)
g1= omdir1['g']
omega_cav1 = omdir1['omega_c']

omdir2 = optomechanics(P_in2, kappa_02, kappa_ex2,
                       omega_cav2, omega_cont2, omega_m, g_02)
g2= omdir2['g']
omega_cav2 = omdir2['omega_c']



a1 = Mode('a1', omega_cav1)
a2 = Mode('a2', omega_cav2)
b = Mode('b', omega_m)

a_cont1 = Input('ex', a1, kappa_ex1, kind = 'drive',
                omega_drive = omega_cont1, bath_temp = T_cont1)
a_in01 = Input('0', a1, kappa_01, kind = 'bath', bath_temp = bath_temp1)

a_cont2 = Input('ex', a2, kappa_ex2, kind = 'drive',
                omega_drive = omega_cont2, bath_temp = T_cont2)
a_in02 = Input('0', a2, kappa_02, kind = 'bath', bath_temp = bath_temp2)

b_in0 = Input('0', b, gamma_m, kind = 'bath', bath_temp=10e-3)

g_a1b = Coupling(a1, b, g1 * np.array([1,0,1,0]))
g_a2b = Coupling(a2, b, g2 * np.array([1,0,0,0]))

sys_om = System([a1, a2, b], [a_in01, a_in02, b_in0, a_cont1, a_cont2],
                [g_a1b, g_a2b])
```

Then we have to define the output ports and then measure the linear response from the input drives port of first cavity to the output port of the second cavity.

```python
a_outex1 = Output(sys_om, a_cont1)
a_outex2 = Output(sys_om, a_cont2)

omegas = np.linspace(omega_cav1 - 2.5* omega_m, omega_cav1 +  2.5 * omega_m, 10000)
omegas_new, A = me.linear_response(omegas, sys_om, a_outex2, a_cont1, plot = True)
```

And the result would be:

<!--
![Frequency conversion linear response amplitude](conv/LR_amp.png){width=460 .center}
\begin{figure}[!h]
\caption{Frequency conversion linear response amplitude}
\end{figure}
-->


<p align="center">
  <img width="460" src="\conv\LR_amp.png">
  <p align = "center">
        Frequency conversion linear response amplitude
  </p>
</p>


Both the input field and output field frequencies are shown on the graph. This means every point on this curve is the amplitude of the output field at the "output frequency", when the input probe is at the corresponding "input frequency".
