"""Kelish yo'nalishi (DoA) algoritmlari: Bartlett va MUSIC."""

from __future__ import annotations

import numpy as np

from .array import AntennaArray

DEFAULT_GRID = np.arange(0.0, 360.0, 0.5)


def spatial_covariance(snapshots: np.ndarray) -> np.ndarray:
    """(M, N) kompleks namunalardan (M kanal, N otschet) kovariatsiya matritsasi."""
    n = snapshots.shape[1]
    return snapshots @ snapshots.conj().T / n


def bartlett_spectrum(
    cov: np.ndarray, array: AntennaArray, frequency_hz: float, grid_deg: np.ndarray = DEFAULT_GRID
) -> np.ndarray:
    """Oddiy beamforming spektri (barqaror, lekin ruxsat etish qobiliyati past)."""
    a = array.steering_matrix(grid_deg, frequency_hz)
    p = np.real(np.sum(a.conj() * (cov @ a), axis=0))
    return p / array.num_elements**2


def music_spectrum(
    cov: np.ndarray,
    array: AntennaArray,
    frequency_hz: float,
    num_sources: int = 1,
    grid_deg: np.ndarray = DEFAULT_GRID,
) -> np.ndarray:
    """MUSIC psevdo-spektri (yuqori ruxsat etish qobiliyati)."""
    m = array.num_elements
    if not 1 <= num_sources < m:
        raise ValueError("num_sources 1 va kanallar_soni-1 oralig'ida bo'lishi kerak")
    _, vecs = np.linalg.eigh(cov)  # o'sish tartibida
    noise = vecs[:, : m - num_sources]
    a = array.steering_matrix(grid_deg, frequency_hz)
    denom = np.sum(np.abs(noise.conj().T @ a) ** 2, axis=0)
    return 1.0 / np.maximum(denom, 1e-12)


def _circular_peaks(spectrum: np.ndarray, count: int) -> list[int]:
    left = np.roll(spectrum, 1)
    right = np.roll(spectrum, -1)
    idx = np.flatnonzero((spectrum > left) & (spectrum >= right))
    return list(idx[np.argsort(spectrum[idx])[::-1][:count]])


def estimate_doa(
    snapshots: np.ndarray,
    array: AntennaArray,
    frequency_hz: float,
    num_sources: int = 1,
    method: str = "music",
    grid_deg: np.ndarray = DEFAULT_GRID,
) -> list[float]:
    """Manbalar azimutlarini (gradus, kuchli cho'qqidan boshlab) qaytaradi."""
    cov = spatial_covariance(snapshots)
    if method == "music":
        spec = music_spectrum(cov, array, frequency_hz, num_sources, grid_deg)
    elif method == "bartlett":
        spec = bartlett_spectrum(cov, array, frequency_hz, grid_deg)
    else:
        raise ValueError(f"noma'lum usul: {method!r} (music yoki bartlett)")
    return [float(grid_deg[i]) for i in _circular_peaks(spec, num_sources)]
