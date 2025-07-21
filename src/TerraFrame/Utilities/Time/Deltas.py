# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import bisect
from copy import deepcopy
from importlib import resources
from typing import Optional

import numpy as np

import TerraFrame.Utilities
from TerraFrame.Utilities import BulletinData
from TerraFrame.Utilities import Conversions
from TerraFrame.Utilities.Helpers import clamp
from TerraFrame.Utilities.Time import JulianDate


class LeapSecondHistory:
    """
    This class acts as the data holder for the history of leap seconds and
    associated deltas. The class methods provide basic querying operations on
    the leap second data.

    The leap second history file is read only once and the data is shared
    between all class instances.
    """

    _section_1_data: Optional[
        list[tuple[JulianDate.JulianDate, float, float, float]]] = None
    _section_2_data: Optional[
        list[tuple[JulianDate.JulianDate, int, int]]] = None

    def __init__(self):
        self._file_name = 'TAI_UTC_Delta.txt'

        self._load_data()

        self._boundary = self._section_2_data[0][0]

    def _get_section_and_index(self, jd):
        assert (isinstance(jd, JulianDate.JulianDate))

        jd = jd.round_to_days()

        if jd < self._boundary:
            index = bisect.bisect_left(self._section_1_data, jd,
                                       key=lambda x: x[0])

            index = clamp(index, 0, len(self._section_1_data) - 1)

            if jd == self._section_1_data[index][0].round_to_days():
                return 1, index
            else:
                return 1, None

        else:
            index = bisect.bisect_left(self._section_2_data, jd,
                                       key=lambda x: x[0])

            index = clamp(index, 0, len(self._section_2_data) - 1)

            if jd == self._section_2_data[index][0].round_to_days():
                return 2, index
            else:
                return 2, None

    def is_leap_second_day(self, jd):
        assert (isinstance(jd, JulianDate.JulianDate))

        section, index = self._get_section_and_index(jd)

        if index is not None:
            return True
        else:
            return False

    def get_leap_second_delta(self, jd):
        assert (isinstance(jd, JulianDate.JulianDate))

        section, index = self._get_section_and_index(jd)

        if index is None:
            return None

        if section == 1:
            return self._section_1_data[index][1]
        else:
            return self._section_2_data[index][1]

    def _load_data(self):
        if (LeapSecondHistory._section_1_data is not None and
                LeapSecondHistory._section_2_data is not None):
            return

        data = []

        file = resources.files("TerraFrame.Data").joinpath(self._file_name)

        with file.open('r', encoding='utf-8') as f:
            data = f.readlines()

        LeapSecondHistory._parse_section_1(data)
        LeapSecondHistory._parse_section_2(data)

    @staticmethod
    def _parse_section_1(data: list[str]):
        found_header = False
        parsed_data = []

        for line in data:
            # If we ever hit the second section, we're done
            if line.strip().lower().startswith('# section 2'):
                break

            # Keep looping until we've hit the section 1 header
            if not found_header:
                if line.strip().lower().startswith('# section 1'):
                    found_header = True

                continue

            # Skip headers
            if line.strip().lower().startswith('year'):
                continue

            # Section header is found so we parse the data now
            line_split_str = [x for x in line.strip().split(',')]
            # Using two lists makes type inspection happy
            line_split = [0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0]

            if len(line_split_str) < 9:
                continue

            # First six values are integers
            for i in range(0, 6):
                line_split[i] = int(line_split_str[i])

            # last three are floats
            for i in range(6, 9):
                line_split[i] = float(line_split_str[i])

            jd = JulianDate.julian_date_from_datetime(line_split[0],
                                                      line_split[1],
                                                      line_split[2],
                                                      line_split[3],
                                                      line_split[4],
                                                      line_split[5])

            parsed_data.append(
                [jd, line_split[6], line_split[7], line_split[8]])

        LeapSecondHistory._section_1_data = parsed_data

    @staticmethod
    def _parse_section_2(data: list[str]):
        found_header = False
        parsed_data = []

        for line in data:
            # Keep looping until we've hit the section 2 header
            if not found_header:
                if line.strip().lower().startswith('# section 2'):
                    found_header = True

                continue

            # Skip headers
            if line.strip().lower().startswith('year'):
                continue

            # Section header is found so we parse the data now
            line_split = [int(x) for x in line.strip().split(',')]

            if len(line_split) < 8:
                continue

            jd = JulianDate.julian_date_from_datetime(line_split[0],
                                                      line_split[1],
                                                      line_split[2],
                                                      line_split[3],
                                                      line_split[4],
                                                      line_split[5])

            parsed_data.append([jd, line_split[6], line_split[7]])

        LeapSecondHistory._section_2_data = parsed_data


class Ut1UtcDelta:
    """
    This class acts as a wrapper over the IERS bulletin data and provides
    methods for directly querying the UT1 - UTC delta at a given UTC datetime.
    """

    _abscissa: Optional[list[JulianDate.JulianDate]] = None

    def __init__(self):
        # BulletinData only reads it's data once, so we don't have to worry
        # about instances leading to useless work
        self._bd = BulletinData.BulletinData()
        self._lhs = LeapSecondHistory()

        self._generate_abscissa()

    def get_delta(self, look_up_times):
        look_up_times = TerraFrame.Utilities.Helpers.ensure_iterable(look_up_times)

        deltas = np.zeros((len(look_up_times),))

        for i, jd in enumerate(look_up_times):
            assert (isinstance(jd, JulianDate.JulianDate))

            is_ls_day = self._lhs.is_leap_second_day(jd.round_to_days())
            ls_delta = 0.0
            in_leap_sec = False

            if is_ls_day:
                ls_delta = self._lhs.get_leap_second_delta(jd)

            index = bisect.bisect(Ut1UtcDelta._abscissa, jd) - 1

            # Special case if we're "inside" the leap second
            if (is_ls_day and float(Ut1UtcDelta._abscissa[index + 1] - jd) <=
                    Conversions.seconds_to_days(ls_delta)):
                jd = Ut1UtcDelta._abscissa[index + 1]
                index += 1
                in_leap_sec = True

            # If we're outside the range of data, just use the end values
            index = clamp(index, 0, len(Ut1UtcDelta._abscissa) - 2)

            x1 = Ut1UtcDelta._abscissa[index]
            x2 = Ut1UtcDelta._abscissa[index + 1]

            y1 = self._bd.ut1_utc_delta(index)
            y2 = self._bd.ut1_utc_delta(index + 1)

            # Apply an offset so that the leap second jump doesn't pollute
            # the interpolation. We don't need to apply the offset if we're in
            # the leap second because we handle that by shifting to the next
            # day which bypasses the jump.
            if is_ls_day and not in_leap_sec:
                y2 -= ls_delta

            m = (y2 - y1) / (float(x2 - x1))

            jd = TerraFrame.Utilities.Helpers.clamp(jd, x1, x2)

            deltas[i] = float(m * (jd - x1) + y1)

        if len(deltas) == 1:
            return deltas[0]
        else:
            return deltas

    def _generate_abscissa(self):
        if Ut1UtcDelta._abscissa is None:
            tmp: list[None | JulianDate.JulianDate] = (len(self._bd) * [None])

            # Loop and convert the floating point MJD values into actual JD
            # objects
            for i, mjd_val in enumerate(self._bd.data[:, 0]):
                mjd = JulianDate.JulianDate(mjd_val)
                jd = JulianDate.modified_julian_date_to_julian_date(mjd)

                tmp[i] = jd

            Ut1UtcDelta._abscissa = tmp


class TaiUtcDelta(LeapSecondHistory):
    """
    This class wraps the LeapSecondHistory class and provides
    method for directly getting UT1 - UTC for a given UTC datetime input.
    """

    def __init__(self):
        super().__init__()

    def get_delta(self, look_up_times):
        """
        This function takes in JulianDate (JD) UTC times and returns the TAI -
        UTC delta in seconds for each input time.

        :param look_up_times: Vector (or single value) of lookup times in UTC
        :type look_up_times: JD | list[JD]
        :return: The TAI - UTC delta in seconds
        :rtype: float | np.ndarray[float]
        """

        look_up_times = TerraFrame.Utilities.Helpers.ensure_iterable(look_up_times)

        deltas = np.zeros((len(look_up_times),))

        for i, jd in enumerate(look_up_times):
            assert (isinstance(jd, JulianDate.JulianDate))

            mjd = JulianDate.julian_date_to_modified_julian_date(jd)

            if jd < self._boundary:
                index = bisect.bisect(LeapSecondHistory._section_1_data, jd,
                                      key=lambda x: x[0]) - 1

                if index < 0:
                    # We're before the first valid date. Adjust the date to
                    # return the last good delta
                    mjd = JulianDate.julian_date_to_modified_julian_date(
                        LeapSecondHistory._section_1_data[0][0])
                    index = 0  # Reset to 0 so we get the right a, b, and c

                a = LeapSecondHistory._section_1_data[index][1]
                b = LeapSecondHistory._section_1_data[index][2]
                c = LeapSecondHistory._section_1_data[index][3]

                deltas[i] = a + (mjd - b) * c
            else:
                index = bisect.bisect(LeapSecondHistory._section_2_data, jd,
                                      key=lambda x: x[0]) - 1

                deltas[i] = LeapSecondHistory._section_2_data[index][2]

        if len(deltas) == 1:
            return deltas[0]
        else:
            return deltas


class TaiUtcDeltaInverted(LeapSecondHistory):
    """
    This class wraps the LeapSecondHistory class and provides
    method for directly getting UT1 - UTC for a given TAI datetime input. As
    the name implies, this class provides the deltas for the opposite (e.g.
    inverted) time input as compared to TaiUtcDelta: TAI instead of UTC.
    """

    def __init__(self):
        super().__init__()

    def __len__(self):
        return (len(LeapSecondHistory._section_1_data) + len(
            LeapSecondHistory._section_2_data))

    @staticmethod
    def get_delta(look_up_times):
        """
        This function takes in JulianDate (JD) TAI times and returns the TAI -
        UTC delta in seconds for each input time.

        :param look_up_times: Vector (or single value) of lookup times in TAI
        :type look_up_times: JD | list[JD]
        :return: The TAI - UTC delta in seconds
        :rtype: float | np.ndarray[float]
        """

        if TaiUtcDeltaInverted._section_1_data is None:
            raise RuntimeError('You must initialize TaiUtcDeltaInverted at '
                               'least once before calling this method.')

        d_tai_utc = TaiUtcDelta()

        look_up_times = TerraFrame.Utilities.Helpers.ensure_iterable(look_up_times)

        deltas = np.zeros((len(look_up_times),))

        for i, jd in enumerate(look_up_times):
            assert (isinstance(jd, JulianDate.JulianDate))
            guess = deepcopy(jd)
            guess.time_scale = JulianDate.TimeScales.UTC
            delta_old = 0

            while True:  # This loop takes at most 3 iterations to terminate
                delta = d_tai_utc.get_delta(guess)

                guess -= Conversions.seconds_to_days(delta)
                guess.time_scale = JulianDate.TimeScales.UTC

                if delta == delta_old:
                    delta_old = delta
                    break

                delta_old = delta

            deltas[i] = delta_old

        if len(deltas) == 1:
            return deltas[0]
        else:
            return deltas
