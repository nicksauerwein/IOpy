In this section the different classes and functions of IOpy are introduced. IOpy consists of 4 main scripts including `elements`, `measurement`, `DCnonlinearaity` and `plots`.

# elements
Objects and functions in this script are used for defining the oscillating modes, input-output ports, couplings between different modes and finally the whole system of coupled oscillators.

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
This class represents the Input field coupled to a `Mode`. Inputs can be coherent drives (pumps) or thermal baths where the only difference between them is the rotating frame.
```python
Attributes:
    name: name of the input field.
    mode: the mode which the input is coupled to.
    kind: flag which indicates the input is a pump or a thermal
          bath. 'drive' for a pump and 'bath' for a thermal bath.
    kappa: coupling rate to the mode in rad/sec.
    omega_drive: frequency of the pump fields in rad/sec.
    bath_temp: tempreture of the bath or the pump in Kelvins.
    nbar: average number of thermal photons in the input field.
```
`nbar` is calculated using the formula
$$\bar n =\frac{1}{e^{\frac{\hbar\omega}{kT}}-1}.$$


Methods:
```python
spectrum(self, omegas):
    spectrum of the input field. Here we approximatley take
    the thermal spectrum to be constant near the mode frequency.
    Args:
        omegas: the frequencies vector at which we want to
                calculate the spectrum.
        
    Returns:
            spectrum of the input field in units of number
            of photons.
```
Currently for the input noise spectrum we consider the simplest case that it is a thermal spectrum. In the future this feautre will be added to allow for user defined spectra. This would allow to account for the classical noises of the lasers (phase noise and amplitude noise).

#### Class `Coupling`
Couplings between two `Mode`s using the coupling vector. The coupling vector, $V_g$, is a 4-dimensional vector which is defined in a way that the interaction Hamiltonian for two coupled modes would be

$$H_{int} = 2\hbar(V_{g,1}X_1X_2 + V_{g,1}X_1Y_2 + V_{g,1}Y_1X_2 + V_{g,1}Y_1Y_2).$$

For example for optomechanics the couling vector is

$$V_g = (g, 0, 0, 0).$$
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
Refer to [Equation (1)](http://127.0.0.1:8000/theory/#input-output-formalism) on the Theory page for more information about $M$ and $L$ matrices.

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
    Constructing the scattering matrix of the system for a
    frequency range.
    
    Args:
        omegas: frequencies vector in rad/sec.
        
    Returns:
        Ss: the scattering matrix.
```
Refer to [Equation (3)](http://127.0.0.1:8000/theory/#input-output-formalism) on Theory page for more information about scattering matrix.

#### Class `Output`
This class represents the output field of the system with respect to an input field (in terms of input-output formalism).
```python
Attributes:
    system: the complex system of coupled modes and inputs.
    input: the input field which we want to define its
           output field (in terms of input-output formalism).
    mode: the mode which these input and output fields are coupled.
```

# measurement
Objects and functions in this script are used for measuring the output fields. Different measurement schemes are linear response and spectrum. For more information about the definitions see Paragraph [Measurements](http://127.0.0.1:8000/theory/#measurements) on the theory Page.

#### Class `MeasurementOperator`
This class represents a general measurment with a measurement operator for defining a correlator.

$$Q(\tau) = \langle Q_{ij}Z_{out,i}(0)Z_{out,j}(\tau)\rangle.$$

Where $Q_{ij}$ is the $ij^{th}$ element of the measurement operator.

Refer to [spectra section](http://127.0.0.1:8000/theory/#spectra) of the theory page for more information about the measurement operator.

```python
Attributes:
    Q: the measurment matrix.
    system: the system which the output field is coming from.
    omega_d: the driving frequency of the mode which the
             output field is coming from.
```

#### Class `PowerMeasurement`
This class represents a power measurement scheme object. The correlator function and measurement matrix in this scheme are
$$ Q(\tau) = \langle q(0)q(\tau) + iq(0)p(\tau) - ip(0)q(\tau) + p(0)p(\tau) \rangle ,$$
$$ [Q] = \begin{pmatrix} 1 &i \\ -i &1 \end{pmatrix}. $$
```python
Attributes:
    system: the system which the output field is coming from.
    omega_d: the driving frequency of the mode which the
             output field is coming from.
    Q: the measurment matrix.
```

#### Class `HomodynMeasurement`
This class represents a Homodyn measurement scheme object with a homodyning angle.
The correlator function and measurement matrix in this scheme are
$$ Q(\tau) = \langle \cos^2(\theta) X(0)X(\tau) + \sin(\theta)\cos(\theta) X(0)Y(\tau) + \sin(\theta)\cos(\theta) Y(0)X(\tau) + \sin^2(\theta) Y(0)Y(\tau) \rangle, $$
$$ [Q] = \begin{pmatrix} \cos^2(\theta) &\sin(\theta)\cos(\theta) \\ \sin(\theta)\cos(\theta) &\sin^2(\theta) \end{pmatrix}. $$
```python
Attributes:
    system: the system which the output field is coming from.
    omega_d: the driving frequency of the mode which the
             output field is coming from.
    Q: the measurment matrix.
```

#### Function `linear_response`
This funtion calculates linear response (susceptibility) of the system from one specific input port to an output port in frequency domain.
$$    a_{out} = \chi  a_{in} $$
Refer to [Equation (4)](http://127.0.0.1:8000/theory/#measurements) of linear response section on the theory page for more information about linear response. 
    
    Args:
        Omegas: the frequencies vector we want to claculate
                the linear response for them, in frame of the
                input field (not a rotating frame)
        system: the system which we want to measure its response.
        output: the output port.
        Input: the input port.
        plot: flag, indicates to plot the susceptibilities or not.
        
    Returns:
        omegas_out: the frequencies vector we want to caLculate
                    the linear response for them, in frame of the
                    output field (not a rotating frame)
        chi: the susceptibility we want to measure.

#### Function `spectrum`
The spectrum of an output field. Refer to [spectra section](http://127.0.0.1:8000/theory/#spectra) of the theory page for more information about the spectra. 
    
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
              A list of spectra form different contributions in case of
              components = True. The nth element of the list contains the
              comulative sum of first n contributions.

# DCnonlinearities
Functions in this script are used for calculating the DC shifts resulting form nonlinear effects.

#### Function `Kerr_effect_nbar`
This function findes the steady state average number of photons in an optical cavity with kerr type nonlinearity. It findes the smallest root route of a third order polynomial equation:

$$ (\frac{- \kappa_{ex}P_{in}}{\hbar\omega_{drive}})\bar n^3 + 
   (\Delta^2 + (\frac{\kappa}{2})^2)\bar n^2 + 
   (2K\Delta) \bar n +
   (K^2) = 0$$
   
    Args:
        P_in: input power in Watts.
        kappa_0: cavity intrinsic dissipation rate in rad/sec.
        kappa_ex: input coupling rate in rad/sec.
        omega_c: cavity resonance frequency in rad/sec.
        omega_drive: frequency of the input field in rad/sec.
        K: nonlinearity coefficient in rad/sec.
        
    returns:
        smallest real root of the third order polynomial equation.

#### Function `optomechanics`
This function findes the steady state average number of photons in an optomechanical cavity and also finds the DC shift cavity 
resonance frequency. It uses the `Kerr_effect_nbar()` function to solve the third order equation:
    
$$\bar n ( \frac{\kappa^2}{4} + (\Delta - (\frac{2g_0^2}{\Omega_m})\bar n)^2 ) = \kappa_{ext} \frac{P_{in}}{\hbar\omega_{drive}}$$
    
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

# plots
Functions in this script are for plotting the linear responses and spectra.

#### Function `plot_linear_response`
This function is for plotting the linear response functions. It plots the absolute value and phase of the linear response as well as plotting the linear response in complex space.
        
        Args:
            omegas: the vector containing the frequecnies
                    in rad/sec (not in a rotating frame).
            chi: the linear response function.
            system: the system which the linear response is from.
            output: the output field we that the linear response
                    is calculated for.
            input: the input field we that the linear response
                   is calculated for.

#### Function `plot_spectrum`
This function is for plotting the spectra.
        
        Args:
            omegas: the vector containing the frequecnies
                    in rad/sec (not in a rotating frame).
            spec: the spectrum.
            componenets: flag, indicates to plot different contributions
                         of noise sources in the spectrum or just
                         plot the whole spectrum.
            system: the system which the spectrum is from.