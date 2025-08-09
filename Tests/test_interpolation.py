# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from TerraFrame.Utilities import Interpolation
import numpy as np


def test_interpolation():
    x = np.array([1, 2, 3])
    y = np.array([1, 4, 9])

    f = Interpolation.Interpolation1D(x, y)

    xv = [0.5, 1.5, 2.0, 2.5, 3.0, 3.5]
    yv = f(xv)

    y_answer = [1.0, 2.5, 4.0, 6.5, 9.0, 9.0]

    for i, v in enumerate(yv):
        assert abs(v - y_answer[i]) < 1e-10
