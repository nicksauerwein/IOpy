# Library
In this section different classes, functions and other commands of IOpy are introduced. IOpy has 4 main scripts including `elements`, `measurement`, `DCnonlinearaity` and `plots`.
## elements
Objects and functions in this script are used for defining the oscillating modes, input-output ports, couplings between different modes and finally the whole system of coupled oscillators.
#### Class `Mode`
Harmonic oscillators of any kind can be defined using this class. a `Mode` is an object which has two initial attributes. `name` and `omega` which are symbolic name of the mode and its resonance frequency in Hertz. The total description of the class is as follows:

```python
.. class:: Mode

   oscillationg mode object

   .. attribute:: name
   
       name of the mode
       
   .. attribute:: omega
   
       resonance frequency of the mode in Hertz
       
   .. attribute:: kappa
   
       mode total dissipation rate in Hertz
       
   .. attribute:: omega_rot
   
       frequency at which the mode frame is rotating in Hertz
       
   .. attribute:: driven
   
       flag indicates whether the mode is driven or not
       
   .. property:: omega_d

       returns the frequency of the field which is driving the mode in Hertz
```
#### Class `Input`
#### Class `Coupling`
#### Class `System`
#### Class `Output`

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


Function `System`
```python
sys_om = System[]
print s
```