# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import os
from datetime import datetime
from pathlib import Path

import requests
from platformdirs import PlatformDirs

from . import Helpers


class DataFileManager:
    """
    This class manages a downloadable datafile resource. If the file doesn't
    exist, it's downloaded. If the file does exist, the file is checked for
    against a configurable stale time and redownloaded if needed.
    """
    file_path: Path | None

    def __init__(self, filename, url, stale_age=None):
        self._file_name = filename
        self._url = url
        self._stale_age = stale_age

        package_name = Helpers.get_package_name()
        self._logger = logging.getLogger(package_name)

        self.file_path = None
        self._get_dir()

    def _get_dir(self):
        # If we're running under CI, this is populated. Use this directory
        # for caching
        data_dir = os.environ.get("TERRAFRAME_CI_CACHE_DIR")

        if data_dir is None:
            package_name = Helpers.get_package_name()
            version = Helpers.get_package_version()
            author = Helpers.get_package_author()

            # If we're in a venv, store in that, otherwise use the OS specific
            # location
            venv_dir = os.environ.get("VIRTUAL_ENV")
            if venv_dir:
                data_dir = Path(venv_dir) / "data" / package_name
            else:
                directories = PlatformDirs(package_name, author, version)
                data_dir = directories.user_data_dir

        if not isinstance(data_dir, Path):
            data_dir = Path(data_dir)

        data_dir.mkdir(parents=True, exist_ok=True)

        self._logger.debug(f'Using directory "{data_dir}" for URL '
                           f'"{self._url}"')

        self.file_path = Path(data_dir, self._file_name)

    def is_stale(self):
        if self._stale_age is None:
            return False

        if os.path.exists(self.file_path):
            ct = datetime.fromtimestamp(os.path.getctime(self.file_path))

            if (datetime.now() - ct).seconds > self._stale_age:
                return True

        return False

    def get_file(self, force=False):
        if (os.path.exists(
                self.file_path) and not self.is_stale() and not force):
            self._logger.debug(f'File "{self.file_path}" isn\'t stale. '
                               f'Skipping.')
            return

        self._logger.info(f'Downloading {self._file_name}')
        response = requests.get(self._url)
        response.raise_for_status()

        with open(self.file_path, "wb") as f:
            f.write(response.content)

        return
