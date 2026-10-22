"""Transparent frequency and protection-path bookkeeping."""

from __future__ import annotations

from typing import Iterable


def conditional_risk(
    baseline_frequency_per_year: float,
    material_factor: float = 1.0,
    weld_factor: float = 1.0,
    environment_factor: float = 1.0,
    inspection_factor: float = 1.0,
) -> float:
    """Apply explicitly labelled conditional multipliers.

    The result is a screening index unless every multiplier is calibrated from
    component-year exposure and inspection data.
    """
    values = [baseline_frequency_per_year, material_factor, weld_factor, environment_factor, inspection_factor]
    if any(value < 0 for value in values):
        raise ValueError("all inputs must be non-negative")
    return baseline_frequency_per_year * material_factor * weld_factor * environment_factor * inspection_factor


def mutually_exclusive_paths(
    initiating_frequency_per_year: float, path_probabilities: Iterable[float]
) -> list[float]:
    """Allocate one initiating frequency across mutually exclusive paths."""
    probabilities = [float(value) for value in path_probabilities]
    if initiating_frequency_per_year < 0 or any(value < 0 for value in probabilities):
        raise ValueError("frequencies and probabilities must be non-negative")
    total = sum(probabilities)
    if abs(total - 1.0) > 1e-9:
        raise ValueError("mutually exclusive path probabilities must sum to one")
    return [initiating_frequency_per_year * value for value in probabilities]
