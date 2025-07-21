# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum


class TimeScales(Enum):
    UTC = 1  # Coordinated Universal Time
    TAI = 2  # International Atomic Time
    TT = 3 # Terrestrial Time
    UT1 = 4 # Universal Time
