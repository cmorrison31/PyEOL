[![Test](https://github.com/cmorrison31/TerraFrame/actions/workflows/test.yml/badge.svg)](https://github.com/cmorrison31/TerraFrame/actions/workflows/test.yml)
[![Release](https://github.com/cmorrison31/TerraFrame/actions/workflows/release.yml/badge.svg)](https://github.com/cmorrison31/TerraFrame/actions/workflows/release.yml)
# TerraFrame
TerraFrame is a library for calculating the orientation of the earth relative 
to the Geocentric Celestial Reference System (GCRS). The intended use of 
this library is to provide modeling and simulation software a transformation 
tensor from an Earth Centered Inertial (ECI) reference frame to an Earth 
Centered Earth Fixed (ECEF) reference frame.  

Specifically, this library computes the transformation tensor between the 
GCRS and the International Terrestrial Reference System (ITRS). The 
transformation uses the IAU 2006/2000A precession-nutation theory, 
references systems, J2000 epoch, and associated algorithms. The library 
relies heavily on IERS data for polar motion, nutation corrections, and UT1 - 
UTC deltas.

In order to provide correct time inputs for the IAU 2006/2000A 
algorithms, this library provides leap second aware conversions between TT,
UTC, TAI, and UT1. For speed and reduced complexity, the user is encouraged 
to work in TT or TAI and only convert to or from UTC when absolutely necessary.

![Animation of CGRS to ITRS Transformation](https://raw.githubusercontent.com/cmorrison31/TerraFrame/main/Animations/GCRS_to_ITRS.gif)

![Example of Precession, Nutation, & Polar Motion](https://raw.githubusercontent.com/cmorrison31/TerraFrame/main/Animations/Earth%20Motion%20Example.gif)

# License
This project - except for the IERS data files - is covered under the Mozilla 
Public License Version 2.0 (MPL2). See the LICENSE.txt file for more 
information.

# Acknowledgements and References
This project uses data published by the International Earth Rotation and 
Reference Systems Service (IERS). The original data along with additional 
information can be found on the IERS website: 
[here.](https://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html)

The [Astropy](https://www.astropy.org/) and 
[PyERFA](https://pypi.org/project/pyerfa/) libraries have been used as 
invaluable sources of truth for the testing of TerraFrame.

This project would not have been possible without the technical information 
provided by the following sources:
- Urban, S. E., & Seidelmann, P. K. (Eds.). Explanatory Supplement to the 
Astronomical Almanac (3rd ed.). University Science Books, 2013. ISBN: 
978-1-891389-85-6.
- Gérard Petit and Brian Luzum (Eds.). IERS Conventions (2010), IERS Technical 
Note No. 36, Frankfurt am Main: Verlag des Bundesamts für Kartographie und 
Geodäsie, 2010. ISBN: 3-89888-989-6.

# Acronyms and Abbreviations
| Term | Meaning                                                    |
|------|------------------------------------------------------------|
| CIO  | Celestial Intermediate Origin                              |
| CIP  | Celestial Intermediate Pole                                |
| CIRS | Celestial Intermediate Reference System                    |
| CEO  | Celestial Ephemeris Origin                                 |
| GCRS | Geocentric Celestial Reference System                      |
| IAU  | International Astronomical Union                           |
| IERS | International Earth Rotation and Reference Systems Service |
| ITRF | International Terrestrial Reference Frame                  |
| ITRS | International Terrestrial Reference System                 |
| TAI  | International Atomic Time                                  |
| TIO  | Terrestrial Intermediate Origin                            |
| TIRS | Terrestrial Intermediate Reference System                  |
| TT   | Terrestrial Time                                           |
| UT1  | Universal Time                                             |
| UTC  | Coordinated Universal Time                                 |

