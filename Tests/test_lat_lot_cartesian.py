import math
import random

import pytest

from TerraFrame import Earth


@pytest.fixture
def random_lat_lon_alt():
    n = 10

    lats = [random.uniform(-90, 90) * math.pi / 180 for _ in range(n)]
    lons = [random.uniform(-180, 180) * math.pi / 180 for _ in range(n)]
    alts = [random.uniform(-5000, 100e3) for _ in range(n)]

    return lats, lons, alts


def helper(earth, lat, lon, alt):
    x, y, z = earth.cartesian_from_lat_lon_alt(lat, lon, alt)

    lat_c, lon_c, alt_c = earth.lat_lon_alt_from_cartesian(x, y, z)

    assert -math.pi / 2.0 <= lat_c <= math.pi / 2.0
    assert -math.pi <= lon_c <= math.pi

    assert abs(lat - lat_c) < 1e-10
    assert abs(lon - lon_c) < 1e-10
    # The altitude accuracy isn't as good as latitude and longitude. However,
    # in terms of relative scale, it's still excellent.
    assert abs(alt - alt_c) < 1e-8


def test_lat_lon_cartesian_spherical_earth(random_lat_lon_alt):
    earth = Earth.SphericalEarth()

    for i, (lat, lon, alt) in enumerate(zip(*random_lat_lon_alt)):
        helper(earth, lat, lon, alt)


def test_lat_lon_cartesian_wgs84_earth(random_lat_lon_alt):
    earth = Earth.WGS84Ellipsoid()

    for i, (lat, lon, alt) in enumerate(zip(*random_lat_lon_alt)):
        helper(earth, lat, lon, alt)
