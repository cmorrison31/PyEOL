# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from collections.abc import Iterable


def ensure_iterable(x):
    # treat string-like as scalar
    if isinstance(x, (str, bytes)):
        return [x]
    elif isinstance(x, Iterable):
        return x
    else:
        return [x]


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))
