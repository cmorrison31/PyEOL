# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import TerraFrame
from TerraFrame.Utilities import Conversions
from TerraFrame.Utilities.Time import JulianDate


def main():
    # Set up our JulianDate (JD) datetime object in the familiar UTC timescale.
    jd_utc = JulianDate.julian_date_from_datetime(2025, 6, 27, 14, 5, 37,
                                                  time_scale=JulianDate.TimeScales.UTC)

    # It's best practice to use terrestrial time (TT) as much as possible and
    # only convert back to UTC during post-processing.
    jd_tt = Conversions.utc_to_tt(jd_utc)

    # Create our GCRS -> ITRS transformation class
    ct = TerraFrame.CelestialTerrestrialTransformation()

    # Get the transformation tensor at the given TT datetime.
    t_ig = ct.itrs_to_gcrs(jd_tt)

    print(t_ig)

    # From here, you can use the transformation as needed. You can also easily
    # request the inverse transform via "ct.gcrs_to_itrs(jd_tt)"


if __name__ == "__main__":
    main()
