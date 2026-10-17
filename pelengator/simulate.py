"""Sinov uchun ko'p kanalli SDR namunalari simulyatsiyasi."""

from __future__ import annotations

import numpy as np

from .array import AntennaArray


def simulate_snapshots(
    array: AntennaArray,
    frequency_hz: float,
    azimuths_deg: list[float],
    num_samples: int = 1024,
    snr_db: float = 20.0,
    seed: int | None = None,
) -> np.ndarray:
    """Mustaqil manbalardan (M, N) kompleks namunalar + oq shovqin."""
    rng = np.random.default_rng(seed)
    a = array.steering_matrix(np.asarray(azimuths_deg), frequency_hz)
    k = a.shape[1]
    s = (rng.standard_normal((k, num_samples)) + 1j * rng.standard_normal((k, num_samples))) / np.sqrt(2)
    sigma = 10 ** (-snr_db / 20)
    n = sigma * (
        rng.standard_normal((array.num_elements, num_samples))
        + 1j * rng.standard_normal((array.num_elements, num_samples))
    ) / np.sqrt(2)
    return a @ s + n
