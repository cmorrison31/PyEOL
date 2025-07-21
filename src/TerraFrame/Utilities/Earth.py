# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import math

from TerraFrame.Utilities.Time.JulianDate import JulianDate
from TerraFrame.Utilities import Time


def earth_rotation_angle(time):
    """
    This function computes the earth rotation angle at a given datetime in UT1.

    :param time: JulianDate in UT1
    :return: Earth rotation angle in radians
    :type time: JulianDate
    :rtype: float
    """

    assert (time.time_scale == Time.TimeScales.UT1)

    day_frac = time.day_fraction()
    tu = time - JulianDate.j2000()

    era = 2.0 * math.pi * (
                day_frac + 0.7790572732640 + float(0.00273781191135448 * tu))

    era = math.fmod(era, 2.0 * math.pi)

    return era
