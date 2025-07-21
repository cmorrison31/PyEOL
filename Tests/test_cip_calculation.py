# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import erfa
import numpy as np

from TerraFrame.PrecessionNutation import SeriesExpansion
from TerraFrame.Utilities.Time import JulianDate


def test_cip_calculation():
    se_cip_x = SeriesExpansion.cip_x()
    se_cip_y = SeriesExpansion.cip_y()
    se_cip_sxy2 = SeriesExpansion.cip_sxy2()

    n = 250
    frac = np.linspace(0, 365.25 * 0.25, n)

    cip_x = np.zeros((n,))
    cip_y = np.zeros((n,))
    cip_s = np.zeros((n,))
    cip_x_a = np.zeros((n,))
    cip_y_a = np.zeros((n,))
    cip_s_a = np.zeros((n,))

    for i, val in enumerate(frac):
        jd_tt = (JulianDate.JulianDate.j2000(
            time_scale=JulianDate.TimeScales.TT) + val)
        jdc_tt = JulianDate.julian_terrestrial_time_to_century(jd_tt)

        cip_x[i] = se_cip_x.compute(jdc_tt)
        cip_y[i] = se_cip_y.compute(jdc_tt)
        sxy2 = se_cip_sxy2.compute(jdc_tt)
        cip_s[i] = sxy2 - cip_x[i] * cip_y[i] / 2.0

        jd1, jd2 = jd_tt.integer_part(), jd_tt.fraction_part()

        # Get X, Y, s using IAU 2006/2000A model
        x, y, s = erfa.xys06a(jd1, jd2)

        cip_x_a[i] = x
        cip_y_a[i] = y
        cip_s_a[i] = s

    assert np.max(np.abs(cip_x - cip_x_a)) < 1e-10
    assert np.max(np.abs(cip_y - cip_y_a)) < 1e-10
    assert np.max(np.abs(cip_s - cip_s_a)) < 1e-10
