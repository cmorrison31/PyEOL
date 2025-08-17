# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import importlib.metadata
import sys
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


def get_package_name():
    current_module = sys.modules[__name__]
    package_name = current_module.__package__.split('.')[
        0] if current_module.__package__ else __name__

    return package_name


def get_package_author():
    author = 'cmorrison'  # This isn't cleanly in project.toml

    return author


def get_package_version():
    package_name = get_package_name()

    try:
        version = importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        version = None

    return version
