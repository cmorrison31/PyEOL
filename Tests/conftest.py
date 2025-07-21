# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import platform
import sys
from pathlib import Path


def _get_python_os_tags():
    """Return python and platform tags from env or system."""
    python_ver = os.getenv("PYTEST_PYTHON",
                           f"{sys.version_info.major}.{sys.version_info.minor}")
    platform_name = os.getenv("PYTEST_PLATFORM", platform.system().lower())
    return python_ver, platform_name


def pytest_report_header(config):
    in_ci = os.getenv("CI") == "true"
    python_ver, platform_name = _get_python_os_tags()
    prefix = "GitHub Actions run" if in_ci else "Local test run"
    return f"{prefix}: Python {python_ver} on {platform_name}"


def pytest_configure(config):
    """If no --junitxml given, set a default with python + platform tags."""
    if not config.option.xmlpath:  # xmlpath is None if --junitxml not passed
        python_ver, platform_name = _get_python_os_tags()
        filename = f"test-results-{platform_name}-{python_ver}.xml"
        config.option.xmlpath = Path(filename)
