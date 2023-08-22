"""Defines the Wolfram Alpha prompt template."""
import textwrap

WOLFRAM_ALPHA_TEMPLATE = textwrap.dedent(
    """
                               When using the Wolfram Alpha Oracle, you must call the query method with an `input_str` argument. Optional arguments, such as maxchars can also be passed in.
                               Here are a few examples of how to use the Wolfram Alpha API through the Wolfram Alpha Oracle tool:


Example 1
----------

input_str: 10 densest metals

- Observed Results - 
Input interpretation:
10 densest metallic elements | by mass density

Result:
1 | hassium | 41 g/cm^3 | 
2 | meitnerium | 37.4 g/cm^3 | 
3 | bohrium | 37.1 g/cm^3 | 
4 | seaborgium | 35.3 g/cm^3 | 
5 | darmstadtium | 34.8 g/cm^3 | 
6 | dubnium | 29.3 g/cm^3 | 
7 | roentgenium | 28.7 g/cm^3 | 
8 | rutherfordium | 23.2 g/cm^3 | 
9 | osmium | 22.59 g/cm^3 | 
10 | iridium | 22.56 g/cm^3 | 

Periodic table location:
image: https://www6b3.wolframalpha.com/Calculate/MSP/MSP231019ge21d317638ic9000064icf9g3h4g5idge?MSPStoreType=image/png&s=18

Images:
image: https://www6b3.wolframalpha.com/Calculate/MSP/MSP231119ge21d317638ic900005b65dgd6f55c7h34?MSPStoreType=image/png&s=18
Wolfram Language code: Dataset[EntityValue[{Entity["Element", "Hassium"], Entity["Element", "Meitnerium"], Entity["Element", "Bohrium"], Entity["Element", "Seaborgium"], Entity["Element", "Darmstadtium"], Entity["Element", "Dubnium"], Entity["Element", "Roentgenium"], Entity["Element", "Rutherfordium"], Entity["Element", "Osmium"], Entity["Element", "Iridium"]}, EntityProperty["Element", "Image"], "EntityAssociation"]]

Basic elemental properties:
atomic symbol | all | Bh | Db | Ds | Hs | Ir | Mt | Os | Rf | Rg | Sg
atomic number | median | 106.5
 | highest | 111 (roentgenium)
 | lowest | 76 (osmium)
 | distribution | 
atomic mass | median | 269 u
 | highest | 282 u (roentgenium)
 | lowest | 190.23 u (osmium)
 | distribution | 
half-life | median | 78 min
 | highest | 13 h (rutherfordium)
 | lowest | 4 min (darmstadtium)
 | distribution | 

Thermodynamic properties:
phase at STP | all | solid
(properties at standard conditions)

Material properties:
mass density | median | 32.1 g/cm^3
 | highest | 41 g/cm^3 (hassium)
 | lowest | 22.56 g/cm^3 (iridium)
 | distribution | 
(properties at standard conditions)

Reactivity:
valence | median | 6
 | highest | 7 (bohrium)
 | lowest | 4 (rutherfordium)
 | distribution | 

Atomic properties:
term symbol | all | ^2S_(1/2) | ^3D_3 | ^3F_2 | ^4F_(3/2) | ^4F_(9/2) | ^5D_0 | ^5D_4 | ^6S_(5/2)
(electronic ground state properties)

Abundances:
crust abundance | median | 0 mass%
 | highest | 1.8×10^-7 mass% (osmium)
 | lowest | 0 mass% (8 elements)
human abundance | median | 0 mass%
 | highest | 0 mass% (8 elements)
 | lowest | 0 mass% (8 elements)

Nuclear properties:
half-life | median | 78 min
 | highest | 13 h (rutherfordium)
 | lowest | 4 min (darmstadtium)
 | distribution | 
specific radioactivity | highest | 6.123×10^6 TBq/g (darmstadtium)
 | lowest | 33169 TBq/g (rutherfordium)
 | median | 366018 TBq/g
 | distribution | 

Wolfram|Alpha website result for "10 densest metals":
https://www6b3.wolframalpha.com/input?i=10+densest+metals

"""
)
