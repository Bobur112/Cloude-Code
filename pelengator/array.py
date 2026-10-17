"""Antenna massivi geometriyasi va yo'naltiruvchi (steering) vektorlar."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

C = 299_792_458.0  # yorug'lik tezligi, m/s


@dataclass(frozen=True)
class AntennaArray:
    """Tekislikdagi antenna massivi.

    positions: (M, 2) massiv, elementlarning x (sharq), y (shimol) koordinatalari, metrda.
    Azimut shimoldan soat strelkasi bo'yicha gradusda o'lchanadi.
    """

    positions: np.ndarray

    @property
    def num_elements(self) -> int:
        return self.positions.shape[0]

    def steering_matrix(self, azimuths_deg: np.ndarray, frequency_hz: float) -> np.ndarray:
        """(M, K) yo'naltiruvchi vektorlar matritsasi."""
        az = np.deg2rad(np.atleast_1d(azimuths_deg).astype(float))
        k = 2 * np.pi * frequency_hz / C
        # Kelish yo'nalishi birlik vektori: (sin az, cos az)
        direction = np.stack([np.sin(az), np.cos(az)])  # (2, K)
        phase = k * (self.positions @ direction)  # (M, K)
        return np.exp(1j * phase)


def uniform_linear_array(num_elements: int, spacing_m: float) -> AntennaArray:
    """Chiziqli massiv, x o'qi bo'ylab joylashgan (broadside = shimol)."""
    x = (np.arange(num_elements) - (num_elements - 1) / 2) * spacing_m
    return AntennaArray(np.stack([x, np.zeros_like(x)], axis=1))


def uniform_circular_array(num_elements: int, radius_m: float) -> AntennaArray:
    """Doiraviy massiv: 0..360° bo'ylab bir xil aniqlik beradi (mobil uchun qulay)."""
    ang = 2 * np.pi * np.arange(num_elements) / num_elements
    return AntennaArray(radius_m * np.stack([np.sin(ang), np.cos(ang)], axis=1))
