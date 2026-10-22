"""Comparative material screening; scores are not observed failure rates."""

from __future__ import annotations

import json
from importlib.resources import files
from typing import Any

import numpy as np


def load_material_priors() -> dict[str, Any]:
    """Load the public, evidence-bounded material prior table."""
    resource = files("ammonia_supply_risk").joinpath("data/material_priors.json")
    return json.loads(resource.read_text(encoding="utf-8"))


def material_screening(
    *, n_samples: int = 50_000, seed: int = 20261022, reference: str = "STS316L"
) -> list[dict[str, Any]]:
    """Return P05/P50/P95 relative damage proxies for each material.

    The priors combine direct and analogue evidence into triangular screening
    distributions. The output is a conditional comparison only. It must not
    be multiplied by a component failure rate without exposure and inspection
    data.
    """
    if n_samples < 1000:
        raise ValueError("n_samples must be at least 1000")
    cfg = load_material_priors()
    materials = cfg["materials"]
    if reference not in materials:
        raise KeyError(reference)
    dims = cfg["dimensions"]
    rng = np.random.default_rng(seed)
    weights_raw = np.vstack(
        [rng.uniform(*cfg["weight_ranges"][dim], n_samples) for dim in dims]
    )
    weights = weights_raw / weights_raw.sum(axis=0)
    scores: dict[str, np.ndarray] = {}
    for name, row in materials.items():
        draws = np.vstack(
            [rng.triangular(*row["scores"][dim], n_samples) for dim in dims]
        )
        scores[name] = np.sum(weights * draws, axis=0)
    ref = scores[reference]
    rows: list[dict[str, Any]] = []
    for name, values in scores.items():
        ratio = values / ref
        rows.append(
            {
                "material": name,
                "category": materials[name]["category"],
                "damage_score_p05_p50_p95": [float(x) for x in np.quantile(values, [0.05, 0.5, 0.95])],
                "relative_proxy_vs_reference_p05_p50_p95": [float(x) for x in np.quantile(ratio, [0.05, 0.5, 0.95])],
                "probability_below_reference": float(np.mean(ratio < 1.0)),
                "qualification": materials[name]["qualification"],
                "source_ids": materials[name]["source_ids"],
            }
        )
    return sorted(rows, key=lambda row: row["relative_proxy_vs_reference_p05_p50_p95"][1])
