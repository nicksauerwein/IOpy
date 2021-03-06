In this section the different classes and functions of IOpy are introduced. IOpy consists of 4 main scripts `elements`, `measurement`, `DCnonlinearaity` and `plots`.

# elements
Objects and functions in this script are used to define the oscillating modes, input-output ports, couplings between different modes and finally the whole system of coupled oscillators.

#### Class `Mode`
This class represents the harmonic oscillators modes.
```python
'''
Attributes:
    name: name of the mode.
    omega: resonance frequency of the mode in rad/sec.
    kappa: mode total dissipation rate in rad/sec.
    omega_rot: frequency at which the mode frame is
               rotating in rad/sec.
    driven: flag indicates whether the mode is driven or not.   

Properties:
    omega_d():
       returns the frequency of the field which is driving
       the mode in rad/sec.
'''
```

#### Class `Input`
This class represents the input field coupled to a `Mode`. Inputs can be coherent drives (pumps) or thermal baths where the only difference between them is the rotating frame.

```python
'''
Attributes:
    name: name of the input field.
    mode: the mode which the input is coupled to.
    kind: flag which indicates the input is a pump or a thermal
          bath. 'drive' for a pump and 'bath' for a thermal bath.
    kappa: coupling rate to the mode in rad/sec.
    omega_drive: frequency of the pump fields in rad/sec.
    bath_temp: temperature of the bath or the pump in Kelvins.
    nbar: average number of thermal photons in the input field.
'''
```

`nbar` is calculated using the formula
$$\bar n =\frac{1}{e^{\frac{\hbar\omega}{kT}}-1}.$$


Methods:

```python
'''
spectrum(self, omegas):
    spectrum of the input field. Here we approximately take
    the thermal spectrum to be constant near the mode frequency.
    Args:
        omegas: the frequencies vector at which we want to
                calculate the spectrum.

    Returns:
            spectrum of the input field in units of number
            of photons.
'''
```

Currently for the input noise spectrum we consider the simplest case that it is a thermal spectrum. In future a feature will be added that allows for user defined spectra. This would make it possible to account for the classical noises of the lasers (phase noise and amplitude noise).

#### Class `Coupling`
This class represents the couplings between two `Mode`s using the coupling vector. The coupling vector \(V_g\) is a 4-dimensional vector which is defined in a way that the interaction Hamiltonian for two coupled modes would be

$$H_{\text{int}} = 2\hbar(V_{g,1}X_1X_2 + V_{g,1}X_1Y_2 + V_{g,1}Y_1X_2 + V_{g,1}Y_1Y_2).$$

For optomechanics the couling vector is

$$V_g = (g, 0, 0, 0).$$

```python
'''
Attributes:
    mode1: first mode.
    mode2: second mode.
    vg: coupling vector. a 4-d real vector.
'''
```

Methods:

```python
'''
contains_mode(self, mode):
    indicates if the mode is involved in this coupling or not.

    Args:
        mode: the mode we want to look for.

    Returns:
       'True' if the mode is involved and 'False' for otherwise.
'''
```

#### Class `System`
Defines the complex system made of coupled `Mode`s and `Input`s. Its most important purpose is to calculate the scattering matrix.

```python
'''
Attributes:
    modes: an array of modes in the system.
    inputs: an array of inputs of the system.
    couplings: couplings between the modes of the system.
    M: the M matrix in the relation dZ/dt = M*Z + L*Z_in.
    L: the L matrix in the relation dZ/dt = M*Z + L*Z_in.
'''
```

Refer to [Equation (1)](https://nicksauerwein.github.io/IOpy/theory/#input-output-formalism) on the Theory page for more information on \(M\) and \(L\) matrices.

Methods:

```python
'''
add_mode(self, mode):
    Adding a mode to the system.

    Args:
        mode: the mode we want to add.
'''
```

```python
'''
add_input(self, inp):
    Adding an input to the system.

    Args:
        inp: the input we want to add.
'''
```

```python
'''
add_coupling(self, coup):
    Adding a coupling to the system.

    Args:
        coup: the coupling we want to add.
'''
```

```python
'''
make_ML(self):
    Constructing M and L matrices of the system.
'''
```
```python
'''
SMatrix(self, omegas):
    Constructs the scattering matrix of the system for a
    frequency range.

    Args:
        omegas: frequencies vector in rad/sec.

    Returns:
        Ss: the scattering matrix.
'''
```
Refer to [Equation (3)](https://nicksauerwein.github.io/IOpy/theory/#input-output-formalism) on Theory page for more information about scattering matrix.

#### Class `Output`
This class represents the output field of the system with respect to an input field (in terms of input-output formalism).

```python
'''
Attributes:
    system: the complex system of coupled modes and inputs.
    input: the input field which we want to define its
           output field (in terms of input-output formalism).
    mode: the mode which these input and output fields are coupled.
'''
```

# measurement
Objects and functions in this script are used to perfom measurements on the output fields. The possible measurement schemes are linear response and spectrum. For more information on the definitions see Paragraph [measurements](https://nicksauerwein.github.io/IOpy/theory/#measurements) on the theory Page.

#### Class `MeasurementOperator`
This class represents a general measurement with a measurement matrix for defining a correlator

$$Q(\tau) = \langle Q_{ij}Z_{\text{out},i}(0)Z_{\text{out},j}(\tau)\rangle,$$

where \(Q_{ij}\) is the \(ij^{th}\) element of the measurement matrix.

Refer to the Paragraph [spectra](https://nicksauerwein.github.io/IOpy/theory/#spectra) of the theory Page for more information on the measurement matrix.

```python
'''
Attributes:
    Q: the measurement matrix.
    system: the system which the output field is coming from.
    omega_d: the driving frequency of the mode which the
             output field is coming from.
'''
```

#### Class `PowerMeasurement`
This class represents a power measurement scheme object. The correlator function and measurement matrix in this scheme are
$$ Q(\tau) = \langle X(0)X(\tau) + iX(0)Y(\tau) - iY(0)X(\tau) + Y(0)Y(\tau) \rangle ,$$
$$ [Q] = \begin{pmatrix} 1 &i \\ -i &1 \end{pmatrix}. $$

```python
'''
Attributes:
    system: the system which the output field is coming from.
    omega_d: the driving frequency of the mode which the
             output field is coming from.
    Q: the measurement matrix.
'''
```

#### Class `HomodynMeasurement`
This class represents a Homodyn measurement scheme object with a homodyning angle.
The correlator function and measurement matrix in this scheme are

$$
Q(\tau) = \langle \cos^2(\theta) X(0)X(\tau) + \sin(\theta)\cos(\theta) X(0)Y(\tau)
$$$$\quad\quad\quad + \sin(\theta)\cos(\theta) Y(0)X(\tau) + \sin^2(\theta) Y(0)Y(\tau) \rangle,
$$

$$ [Q] = \begin{pmatrix} \cos^2(\theta) &\sin(\theta)\cos(\theta) \\ \sin(\theta)\cos(\theta) &\sin^2(\theta) \end{pmatrix}. $$

```python
'''
Attributes:
    system: the system which the output field is coming from.
    omega_d: the driving frequency of the mode which the
             output field is coming from.
    Q: the measurement matrix.
'''
```

#### Function `linear_response`

This function calculates linear response (susceptibility) of the system from one specific input port to an output port in frequency domain
$$    a_{\text{out}} = \chi  a_{\text{in}} .$$
Refer to [Equation (4)](https://nicksauerwein.github.io/IOpy/theory/#measurements) of linear response Paragraph on the theory Page for more information on linear response.

```python
'''    
    Args:
        Omegas: the frequencies vector we want to calculate
                the linear response for them, in frame of the
                input field (not a rotating frame)
        system: the system which we want to measure its response.
        output: the output port.
        Input: the input port.
        plot: flag, indicates to plot the susceptibilities or not.

    Returns:
        omegas_out: the frequencies vector we want to calculate
                    the linear response for them, in frame of the
                    output field (not a rotating frame)
        chi: the susceptibility we want to measure.
'''
```

#### Function `spectrum`
The spectrum of an output field. Refer to [spectra](https://nicksauerwein.github.io/IOpy/theory/#spectra) Paragraph on the theory Page for more information on the spectra.

```python
'''
    Args:
        omegas: the frequencies vector we want to calculate the
                spectrum for them, in frame of the output field
                (not a rotating frame)
        measurement: the measurement scheme, of kinds PowerMeasurement
                     or HomodynMeasurement or another general measurement.
        components: flag, indicates to calcuate different contributions
                    of noise sources or just calculate the whole spectrum.
        plot: flag, indicates to plot the spectra or not.

    Returns:
        spec: the spectrum of the output field in case of components = False.
              A list of spectra from different contributions in case of
              components = True. The nth element of the list contains the
              comulative sum of first n contributions.
'''
```

# DCnonlinearities
Functions in this script are used to calculate the DC shifts resulting from nonlinear effects.

#### Function `Kerr_effect_nbar`
This function finds the steady state average photon number in an optical cavity with kerr type nonlinearity. It findes the smallest root of a third order polynomial equation:

$$ [\frac{- \kappa_{\text{ex}}P_{\text{in}}}{\hbar\omega_{\text{drive}}}]\bar n^3 +
   (\Delta^2 + (\frac{\kappa}{2})^2)\bar n^2 +
   (2K\Delta) \bar n +
   (K^2) = 0$$

```python
'''
    Args:
        P_in: input power in Watts.
        kappa_0: cavity intrinsic dissipation rate in rad/sec.
        kappa_ex: input coupling rate in rad/sec.
        omega_c: cavity resonance frequency in rad/sec.
        omega_drive: frequency of the input field in rad/sec.
        K: nonlinearity coefficient in rad/sec.

    returns:
        smallest real root of the third order polynomial equation.
'''
```

#### Function `optomechanics`
This function finds the steady state average photon number in an optomechanical cavity and also finds the DC shift cavity
resonance frequency. It uses the `Kerr_effect_nbar()` function to solve the third order equation

$$\bar n [ \frac{\kappa^2}{4} + (\Delta - (\frac{2g_0^2}{\Omega_m})\bar n)^2 ] = \kappa_{\text{ext}} \frac{P_{\text{in}}}{\hbar\omega_{\text{drive}}}.$$

```python
'''    
    Args:
        P_in: input power in Watts.
        kappa_0: cavity intrinsic dissipation rate in rad/sec.
        kappa_ex: input coupling rate in rad/sec.
        omega_c: cavity resonance frequency in rad/sec.
        omega_drive: frequency of the input field in rad/sec.
        omega_m: resonance frequency of the mechanical oscillator in rad/sec.
        g_0:  vacuum optomechanical coupling rate in rad/sec.

    returns:
        omega_c: modified cavity resonance frequency in rad/sec.
        g: optomechanical coupling rate in rad/sec.
'''
```

# plots
Functions in this script can be used for plotting the linear responses and spectra.

#### Function `plot_linear_response`
This function is used for plotting the linear response functions. It plots the absolute value and phase of the linear response as well as the linear response as a trajectory in the complex plane.

```python
'''
        Args:
            omegas: the vector containing the frequencies
                    in rad/sec (not in a rotating frame).
            chi: the linear response function.
            system: the system which the linear response is from.
            output: the output field we that the linear response
                    is calculated for.
            input: the input field we that the linear response
                   is calculated for.
'''
```

#### Function `plot_spectrum`
This function is used for plotting the spectra.

```python
'''        
        Args:
            omegas: the vector containing the frequencies
                    in rad/sec (not in a rotating frame).
            spec: the spectrum.
            componenets: flag, indicates to plot different contributions
                         of noise sources in the spectrum or just
                         plot the whole spectrum.
            system: the system which the spectrum is from.
'''
```
