# Examples
In this section a set famous phenomena in optomechanics context are presented. These calculations are first as examples of using IOpy in simulating Langevin equations, and second are benchmarks which results of IOpy can be compared against results which are theoretically developed.

## Simple Cavity 

<p align="left">
  <img width="260" src="\LC.png">
</p>

The first example is simulating a hot microwave resonator. Here the temperature of the bath is higher than the temperature of the drive and therefore we would expect to see an emmition shaped like a Lorenzian. To see the fool written example, go to [Simple cavity example](http://localhost:8888/notebooks/IOpy/iopy/examples/Simple%20Cavity.ipynb).
<br />first we have to define the cavity mode:
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

a_inex = Input('ex', a, kappa_ex, kind = 'drive', omega_drive = omega_c, bath_temp=T_drive)
a_in0 = Input('0', a, kappa_0, kind = 'bath', bath_temp=T_bath)
```
And finally the system object and the output field.
```python
sys_cav = System([a], [a_in0,  a_inex], [])
```
```python
a_outex = Output(sys_cav, a_inex)
```
Now for measuring the spectrum  of the output field, we have to use the `spectrum` function:
```python
omegas = np.linspace( omega_c - 15*kappa, omega_c +  15*kappa, 1001)
spec = me.spectrum(omegas, me.PowerMeasurement(a_outex), components = False, plot = True)
```

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

The results can also be compared to the theory. For example in this case the linear response of the system to the drive field is:

$$ S_{aa} = 1 - \frac{\kappa_{ex}}{\frac{\kappa}{2} - i(\omega-\omega_c)} $$

The graphs below show the comparison between this equation and IOpy results.


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


## Basic optomechanics and cooling
<p align="left">
  <img width="260" src="\drum.png">
</p>

          
In this example we simulate an optomechanical system with a weak drive. Here we want to see the optomechanical cooling due to increase in optomechanical damping rate. To see the fool written example, go to [Basic optomechanics](http://localhost:8888/notebooks/IOpy/iopy/examples/Basic%20Optomechanics.ipynb).

In the basic optomechanical interaction, the cavity resonance frequency shift by a constant value due to DC nonlinearity. Therefore, before difining the modes we have to calculate this DC shift.

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

omdir = optomechanics(P_in, kappa_0, kappa_ex, omega_c, omega_drive, omega_m, g_0)

g= omdir['g']                # optomechanical coupling rate = sqrt(nbar) * g_0
omega_c = omdir['omega_c']   # new cavity resonance frequency
```
Now we can define the modes, as well as input fields including thermal baths coupled to optics and mechanics and the optical driving field.

```python
a = Mode('a', omega_c)
b = Mode('b', omega_m)

a_inex = Input('ex', a, kappa_ex, kind = 'drive', omega_drive = omega_drive, bath_temp=10e-3)
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

<p align="center">
  <img width="460" src="\Basic OM\spec.png">
    <p align = "center">
        optomechanical cavity output spectrum
    </p>
</p>

The peak that can be seen is because of low sampling rate of the calculations. To have a better precission we zoom on the neighbourhood of the cavity resonance frequency.

<p align="center">
  <img width="460" src="\Basic OM\spec_zoom.png">
    <p align = "center">
        optomechanical cavity output spectrum
    </p>
</p>

Here we can clearly see different contribuitions to the spectrum. In addition the width of the spectrum is equal to the theory value $\Gamma_{eff} = \Gamma_m (1 + C)$ (with $C$ as the cooperativity equal to $\frac{4g^2}{\kappa\Gamma_m}$) which results to cooling.


## Strong coupling regime
<p align="left">
  <img width="260" src="\Strong.png">
</p>


In this example we show the effect of increasing of the laser input power ($P_{in}$). For the details on the theory see [(Aspelmeyer, Kippenberg, Marquardt (2014))](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.86.1391), section VII.C. By increasing the input power, at the beginning will only see an imporevement in the cooling, but as we continue with increasing the power the optical and mechanical modes hybridize to form two new modes with the eigenfrequencies:

$$ \omega_{\pm} = \frac{\Omega_m-\Delta}{2} \pm \sqrt{g^2 + (\frac{\Omega_m+\Delta}{2})^2}$$

When the driving laser is exactly detuned on the red sideband ($\Delta=-\Omega_m$) the splitting of these two modes is equal to $2g$. In this example we want to show this splitting on the spectrum.

To this end, the code is exactly the same as the previous example but with a different input power. To see the full code go to [Strong coupling regime](http://localhost:8888/notebooks/IOpy/iopy/examples/Strong%20Coupling%20Regime.ipynb). 
```python
P_in = 5e-9
```
By measuring the output filed spectrum we can clearly see this mode splitting:
<p align="center">
  <img width="460" src="\Strong coupling\spec0.png">
    <p align = "center">
        optomechanical cavity output spectrum
    </p>
</p>
To see better the splitting we change the measurement frequencies:
<p align="center">
  <img width="460" src="\Strong coupling\spec.png">
    <p align = "center">
        optomechanical cavity output spectrum
    </p>
</p>

## OMIT
[OMIT](http://localhost:8888/notebooks/IOpy/iopy/examples/OMIT.ipynb)

## Frequency conversion using OMIT

## Ponderomotive squeezing