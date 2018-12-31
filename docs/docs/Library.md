# Library
In this section different classes, functions and other commands of IOpy are introduced. IOpy has 4 main scripts including `elements`, `measurement`, `DCnonlinearaity` and `plots`.
## elements
Objects and functions in this script are used for defining the oscillating modes, input-output ports, couplings between different modes and finally the whole system of coupled oscillators.
#### Class `Mode`
Harmonic oscillators of any kind can be defined using this class.
```python
Attributes:
    name: name of the mode.
    omega: resonance frequency of the mode in rad/sec.
    kappa: mode total dissipation rate in rad/sec.
    omega_rot: frequency at which the mode frame is rotating in rad/sec.
    driven: flag indicates whether the mode is driven or not.   

Properties:
    omega_d():
       returns the frequency of the field which is driving the mode in rad/sec.
```
#### Class `Input`
Input field coupled to a `Mode`. Inputs can be coherent drives (pumps) or thermal baths.
```python
Attributes:
    name: name of the input field.
    mode: the mode which the input is coupled to.
    kind: flag which indicates the input is a pump or a thermal bath.
          'drive' for a pump and 'bath' for a thermal bath.
    kappa: coupling rate to the mode in rad/sec.
    omega_drive: frequency of the pump fields in rad/sec.
    bath_temp: tempreture of the bath or the pump in Kelvins.
    nbar: average number of thermal photons in the input field.
```
`nbar` is calculated using the formula:
$$\bar n =\frac{1}{e^{\frac{\hbar\omega}{kT}}-1}$$


Methods:
```python
spectrum(self, omegas):
    spectrum of the input field. Here we approximatley take the thermal spectrum to be flat near the mode frequency.
    Args:
        omegas: the frequencies vector at which we want to calculate the spectrum.
        
    Returns:
            spectrum of the input field in units of number of photons.
```
#### Class `Coupling`
Couplings between two `Mode`s using the coupling vector. The coupling vector, $V_g$, is a 4-dimensional vector which is defined in a way that the interaction Hamiltonian for two coupled modes would be:

$$H_{int} = 4\hbar(V_{g,1}q_1q_2 + V_{g,1}q_1p_2 + V_{g,1}p_1q_2 + V_{g,1}p_1p_2)$$

For example for optomechanics the couling vector is:

$$V_g = (g, 0, 0, 0)$$
```python
Attributes:
    mode1: first mode.
    mode2: second mode.
    vg: coupling vector. a 4-d real vector.    
```
Methods:
```python
contains_mode(self, mode):
    indicates if the mode is involved in this coupling or not.
        
    Args:
        mode: the mode we want to look for.

    Returns:
        'True' if the mode is involved and 'False' for other wise.
```
#### Class `System`
Defines the complex system made of coupled `Mode`s and `Input`s. It's most important purpose of it is for calculating the scattering matrix.
```python
Attributes:
    modes: an array of modes in the system.
    inputs: an array of inputs of the system.
    couplings: couplings between the modes of the system.
    M: the M matrix in the relation dZ/dt = M*Z + L*Z_in.
    L: the L matrix in the relation dZ/dt = M*Z + L*Z_in.
```
Refer to [Equation (1)](http://127.0.0.1:8000/theory/#input-output-formalism) for more about $M$ and $L$ matrices.

Methods:
```python
add_mode(self, mode):
    Adding a mode to the system.
        
    Args:
        mode: the mode we want to add.
```

```python
add_input(self, inp):
    Adding an input to the system.

    Args:
        inp: the input we want to add.
```

```python
add_coupling(self, coup):
    Adding a coupling to the system.

    Args:
        coup: the coupling we want to add.
```

```python
make_ML(self):
    Constructing M and L matrices of the system.
```
```python
SMatrix(self, omegas):
    Constructing the scattering matrix of the system for a frequency range.
    
    Args:
        omegas: frequencies vector in rad/sec.
        
    Returns:
        Ss: the scattering matrix.
```
Refer to [Equation (4)](http://127.0.0.1:8000/theory/#input-output-formalism) for more about scattering matrix.
#### Class `Output`
The output field of the system with respect to an input field (in terms of input-output formalism).
```python
Attributes:
    system: the complex system of coupled modes and inputs.
    input: the input field which we want to define its output field (in terms of input-output formalism).
    mode: the mode which these input and output fields are coupled.
```
## measurement

#### Class `MeasurementOperator`
#### Class `PowerMeasurement`
#### Class `HomodynMeasurement`
#### Function `linear_response`
#### Function `spectrum`

## DCnonlinearities

#### Function `Kerr_effect_nbar`
#### Function `optomechanics`

## plots

#### Function `plot_linear_response`
#### Function `plot_spectrum`