# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import random
from importlib import resources

import astropy.time
import astropy.units as u
import erfa
import numpy as np
from astropy.coordinates import GCRS, ITRS, CartesianRepresentation
from astropy.utils import iers
from astropy.utils.iers import IERS_A

import TerraFrame
from TerraFrame.Utilities import Conversions
from TerraFrame.Utilities.Time import JulianDate


def test_itrs_to_gcrs_calculation():
    val = random.uniform(0, 100.0)
    jd_utc = JulianDate.JulianDate.j2000() + val
    jd_tt = Conversions.utc_to_tt(jd_utc)
    jd_ut1 = Conversions.utc_to_ut1(jd_utc)

    # No corrections since we're comparing against a bare ERFA routine
    ct = (TerraFrame.CelestialTerrestrialTransformation(user_polar_motion=False,
        user_nutation_corrections=False))

    t_ig = ct.itrs_to_gcrs(jd_tt)

    tta, ttb = jd_tt.integer_part(), jd_tt.fraction_part()
    ut1a, ut1b = jd_ut1.integer_part(), jd_ut1.fraction_part()
    xp = 0.0
    yp = 0.0
    t_gi_erfa = erfa.c2t06a(tta, ttb, ut1a, ut1b, xp, yp)
    t_ig_erfa = np.transpose(t_gi_erfa)

    assert (np.max(np.abs(t_ig - t_ig_erfa)) < 1e-10)


def test_against_astropy():
    val = random.uniform(0, 9000.0)
    jd_utc = JulianDate.JulianDate.j2000() + val

    gcrs_basis = np.eye(3)

    # Apparently, Astropy doesn't use the dx and dy nutation corrections.
    # See: https://github.com/astropy/astropy/issues/11110
    ct = (TerraFrame.CelestialTerrestrialTransformation(user_polar_motion=True,
        user_nutation_corrections=False))

    t_ig = ct.gcrs_to_itrs(jd_utc)

    itrs_basis = t_ig @ gcrs_basis

    file_name = "finals.all.iau2000.txt"
    file_path = resources.files("TerraFrame.Data").joinpath(file_name)

    with resources.as_file(file_path) as path:
        iers_table = IERS_A.open(str(path))
        iers.earth_orientation_table.set(iers_table)

    # noinspection PyUnresolvedReferences
    t = astropy.time.Time(jd_utc.integer_part(), jd_utc.fraction_part(),
                          format='jd', scale='utc')

    gcrs_basis_astro = GCRS(CartesianRepresentation(gcrs_basis, unit=u.one),
                            obstime=t)
    itrs_basis_astro = gcrs_basis_astro.transform_to(ITRS(obstime=t))
    itrs_basis_astro = itrs_basis_astro.cartesian.xyz.to_value()

    assert (np.max(np.abs(itrs_basis - itrs_basis_astro)) < 1e-10)


def test_leap_second_against_astropy():
    jd_utc_base = JulianDate.julian_date_from_datetime(2015, 6, 30, 23, 59, 58,
                                                       time_scale=JulianDate.TimeScales.UTC)
    jd_tt_base = Conversions.utc_to_tt(jd_utc_base)
    gcrs_basis = np.eye(3)

    # Apparently, Astropy doesn't use the dx and dy nutation corrections.
    # See: https://github.com/astropy/astropy/issues/11110
    ct = (TerraFrame.CelestialTerrestrialTransformation(user_polar_motion=True,
        user_nutation_corrections=False))

    file_name = "finals.all.iau2000.txt"
    file_path = resources.files("TerraFrame.Data").joinpath(file_name)

    with resources.as_file(file_path) as path:
        iers_table = IERS_A.open(str(path))
        iers.earth_orientation_table.set(iers_table)

    for delta in [0, 1.0, 1.5, 2.0, 3.0, 4.0]:
        jd_tt = jd_tt_base + Conversions.seconds_to_days(delta)

        t_ig = ct.gcrs_to_itrs(jd_tt)

        itrs_basis = t_ig @ gcrs_basis

        # noinspection PyUnresolvedReferences
        t = astropy.time.Time(jd_tt.integer_part(), jd_tt.fraction_part(),
                              format='jd', scale='tt')

        gcrs_basis_astro = GCRS(CartesianRepresentation(gcrs_basis, unit=u.one),
                                obstime=t)
        itrs_basis_astro = gcrs_basis_astro.transform_to(ITRS(obstime=t))
        itrs_basis_astro = itrs_basis_astro.cartesian.xyz.to_value()

        assert (np.max(np.abs(itrs_basis - itrs_basis_astro)) < 1e-10)
