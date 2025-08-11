[![Test](https://github.com/cmorrison31/TerraFrame/actions/workflows/test.yml/badge.svg)](https://github.com/cmorrison31/TerraFrame/actions/workflows/test.yml)
[![Release](https://github.com/cmorrison31/TerraFrame/actions/workflows/release.yml/badge.svg)](https://github.com/cmorrison31/TerraFrame/actions/workflows/release.yml)

# TerraFrame

TerraFrame is a library designed to provide earth-orientation functionally to
modeling and simulation software by calculating a transformation 
tensor between the Geocentric Celestial Reference System (GCRS) and the 
International Terrestrial Reference System (ITRS). This transformation accounts for 
precession, nutation, and polar motion using the IAU 2006/2000A 
precession-nutation theory and IERS data files.  

Additionally, support is provided for converting between geodetic latitude, 
longitude and height above ellipsoid and geocentric cartesian coordinates or 
vice versa. The WGS84 spheroid and a simple spherical earth are provided as 
built-in options.

TerraFrame provides robust datetime and timescale conversion functionality that
is fully leap second aware. Conversions between UTC, UT1, TT, and TAI are
provided. The user is encouraged to not work in UTC directly to avoid
leap second ambiguity. Conversion to UTC from TT or TAI can be safely done
in post-processing.

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

