# Examples
In this section a set famous phenomena in optomechanics context are presented. These calculations are first as examples of using IOpy in simulating Langevin equations, and second are benchmarks which results of IOpy can be compared against results which are theoretically developed.

# Simple Cavity 
<p align="left">
  <img width="260" src="\LC.png">
</p>
The first example is simulating a hot microwave resonator. Here the temperature of the bath is higher than the temperature of the drive and therefore we would expect to see an emmition shaped like a Lorenzian. to see the fool written example, go to [Simple cavity example](http://localhost:8888/notebooks/IOpy/iopy/examples/Simple%20Cavity.ipynb).
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

<p align="center">
  <img width="460" src="\simple_cavity_spectrum.png">
</p>


# Basic optomechanics
[Basic optomechanics](http://localhost:8888/notebooks/IOpy/iopy/examples/Basic%20Optomechanics.ipynb)

# Strong coupling regime
[Strong coupling regime](http://localhost:8888/notebooks/IOpy/iopy/examples/Strong%20Coupling%20Regime.ipynb)

# OMIT
[OMIT](http://localhost:8888/notebooks/IOpy/iopy/examples/OMIT.ipynb)

# Frequency conversion using OMIT

# Ponderomotive squeezing