# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import random

import erfa
import numpy as np

from TerraFrame.PrecessionNutation import SeriesExpansion
from TerraFrame.Utilities import TransformationMatrices
from TerraFrame.Utilities.Time import JulianDate


def test_cirs_to_gcrs_calculation():
    se_cip_x = SeriesExpansion.cip_x()
    se_cip_y = SeriesExpansion.cip_y()
    se_cip_sxy2 = SeriesExpansion.cip_sxy2()

    val = random.uniform(0, 100.0)
    jd_tt = (JulianDate.JulianDate.j2000(
        time_scale=JulianDate.TimeScales.TT) + val)
    jdc_tt = JulianDate.julian_terrestrial_time_to_century(jd_tt)

    cip_x = se_cip_x.compute(jdc_tt)
    cip_y = se_cip_y.compute(jdc_tt)
    sxy2 = se_cip_sxy2.compute(jdc_tt)
    cip_s = sxy2 - cip_x * cip_y / 2.0

    t_gc = TransformationMatrices.cirs_to_gcrs(cip_x, cip_y, cip_s)

    jd1, jd2 = jd_tt.integer_part(), jd_tt.fraction_part()

    # Get X, Y, s using IAU 2006/2000A model
    x, y, s = erfa.xys06a(jd1, jd2)

    # ERFA/SOFA computes the inverse transform, so we need to take the transpose
    t_cg_erfa = erfa.c2ixys(x, y, s)
    t_gc_erfa = t_cg_erfa.T

    assert abs(cip_x - x) < 1e-8
    assert abs(cip_y - y) < 1e-8
    assert abs(cip_s - s) < 1e-8

    assert (np.max(np.abs(t_gc - t_gc_erfa)) < 1e-10)
