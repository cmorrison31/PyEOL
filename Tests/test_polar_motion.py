# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import random

import erfa
import numpy as np

from TerraFrame.Utilities import TransformationMatrices
from TerraFrame.Utilities.Time import JulianDate


def test_s_prime():
    val = random.uniform(0, 100.0)
    jd_tt = (JulianDate.JulianDate.j2000(
        time_scale=JulianDate.TimeScales.TT) + val)
    jdc_tt = JulianDate.julian_terrestrial_time_to_century(jd_tt)

    s_p = TransformationMatrices.calculate_s_prime(jdc_tt)

    jd1, jd2 = jd_tt.integer_part(), jd_tt.fraction_part()
    s_p_a = erfa.sp00(jd1, jd2)

    assert (abs(s_p - s_p_a) < 1e-10)


def test_itrs_to_tirs():
    val = random.uniform(0, 100.0)
    pm_x = random.uniform(0, 1e-3)
    pm_y = random.uniform(0, 1e-3)

    jd_tt = (JulianDate.JulianDate.j2000(
        time_scale=JulianDate.TimeScales.TT) + val)
    jdc_tt = JulianDate.julian_terrestrial_time_to_century(jd_tt)

    s_p = TransformationMatrices.calculate_s_prime(jdc_tt)

    t_ti = TransformationMatrices.itrs_to_tirs(pm_x, pm_y, s_p)

    jd1, jd2 = jd_tt.integer_part(), jd_tt.fraction_part()
    s_p_a = erfa.sp00(jd1, jd2)

    # ERFA/SOFA computes the inverse transform, so we need to take the transpose
    t_it_erfa = erfa.pom00(pm_x, pm_y, s_p_a)
    t_ti_erfa = t_it_erfa.T

    assert (np.max(np.abs(t_ti - t_ti_erfa)) < 1e-10)
