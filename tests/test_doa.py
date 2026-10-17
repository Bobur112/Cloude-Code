import numpy as np
import pytest

from pelengator import (
    estimate_doa,
    simulate_snapshots,
    uniform_circular_array,
    uniform_linear_array,
)

FREQ = 433e6
WAVELENGTH = 299_792_458.0 / FREQ


def _angdiff(a, b):
    return abs((a - b + 180) % 360 - 180)


@pytest.mark.parametrize("method", ["music", "bartlett"])
@pytest.mark.parametrize("az", [0.0, 42.0, 135.0, 270.0, 359.0])
def test_single_source_circular(method, az):
    arr = uniform_circular_array(5, 0.5 * WAVELENGTH / (2 * np.sin(np.pi / 5)))
    x = simulate_snapshots(arr, FREQ, [az], snr_db=15, seed=1)
    (est,) = estimate_doa(x, arr, FREQ, 1, method)
    assert _angdiff(est, az) <= 2.0


def test_two_sources_music():
    arr = uniform_circular_array(6, 0.5 * WAVELENGTH / (2 * np.sin(np.pi / 6)))
    x = simulate_snapshots(arr, FREQ, [60.0, 200.0], snr_db=20, seed=2)
    est = estimate_doa(x, arr, FREQ, 2, "music")
    for truth in (60.0, 200.0):
        assert min(_angdiff(e, truth) for e in est) <= 2.0


def test_linear_array_broadside():
    arr = uniform_linear_array(6, 0.5 * WAVELENGTH)
    x = simulate_snapshots(arr, FREQ, [20.0], snr_db=20, seed=3)
    (est,) = estimate_doa(x, arr, FREQ, 1, "music", grid_deg=np.arange(-90, 90, 0.5))
    assert abs(est - 20.0) <= 1.0


def test_invalid_args():
    arr = uniform_circular_array(4, 0.2)
    x = simulate_snapshots(arr, FREQ, [10.0], seed=0)
    with pytest.raises(ValueError):
        estimate_doa(x, arr, FREQ, 4, "music")
    with pytest.raises(ValueError):
        estimate_doa(x, arr, FREQ, 1, "capon")
