# ammonia-supply-risk

Evidence-bounded screening utilities for ammonia supply-system studies. This small Python package publishes the reproducible core calculation examples from the underlying research: comparative material damage proxies, transparent conditional multipliers, and mutually exclusive protection-path bookkeeping.

**The outputs support comparative screening. Material scores are not measured annual leak frequencies, and this package is not a complete facility risk model.**

## Installation

Requires Python 3.10 or later and NumPy 1.24 or later.

```console
python -m pip install ammonia-supply-risk
```

For development from this repository:

```console
git clone https://github.com/lyullee/ammonia-supply-risk.git
cd ammonia-supply-risk
python -m pip install -e .
```

## Included calculations

| Function or data | Purpose | Interpretation |
| --- | --- | --- |
| `material_screening` | Compare 10 materials, including STS304, STS316L, and STS317 | Samples triangular material priors and normalized uncertain weights; returns conditional damage proxies |
| `conditional_risk` | Multiply a declared baseline by material, weld, environment, and inspection factors | A screening index unless the baseline and every multiplier have an adequate empirical calibration |
| `mutually_exclusive_paths` | Allocate one initiating frequency across exclusive protection paths | Probabilities must sum to one; the initiating frequency is allocated once |
| `data/qualified_sobol_summary.csv` | Inspect the archived summary for seven outputs that passed the research convergence criteria | A saved research result, not a Sobol analysis rerun by these three functions |

## Reproducible Python example

```python
from ammonia_supply_risk import (
    conditional_risk,
    material_screening,
    mutually_exclusive_paths,
)

rows = material_screening(
    n_samples=10_000,
    seed=20261022,
    reference="STS316L",
)
for row in rows:
    print(row["material"], row["relative_proxy_vs_reference_p05_p50_p95"])

# Illustrative assumptions only; the multiplier is not a measured material rate.
screening_index = conditional_risk(1.0e-4, material_factor=1.2)
print(screening_index)  # approximately 0.00012

# Allocate the same initiating frequency once across two exclusive paths.
path_frequencies = mutually_exclusive_paths(1.0e-4, [0.2, 0.8])
print(path_frequencies)  # approximately [0.00002, 0.00008]
```

`material_screening` returns a list of dictionaries sorted by the median relative proxy. Each row includes the material/category, P05/P50/P95 damage score, P05/P50/P95 ratio to the reference, probability of a lower proxy than the reference, evidence qualification, and source identifiers. The STS316L self-reference ratio is one. `probability_below_reference` concerns the sampled proxy, not the probability of an actual leak.

At least 1,000 samples are required. An unknown reference raises `KeyError`. Conditional multipliers must be non-negative. Path probabilities must be non-negative and sum to one within `1e-9`. These checks are input guards; users must also supply finite, physically meaningful values.

## Evidence and applicability

Material priors combine direct and analogue evidence into screening distributions. Actual material-specific failure frequencies require component-year exposure, failure counts, crack-growth information, initial-defect distributions, failure criteria, and inspection probability of detection (POD). The package does not derive those data from a material ranking.

It does not calculate ammonia dispersion, exposure consequences, or a complete annual facility QRA. Do not automatically insert the material proxy into a calibrated component failure-rate model. Preserve assumptions and evidence qualifications with any reported result.

The public archive excludes paper full texts, proprietary simulator files, external code, and raw source datasets whose redistribution rights were not established. See [NOTICE.md](NOTICE.md) for the distribution notice.

## Development check

From a source checkout, install pytest and run the existing public-API tests:

```console
python -m pip install pytest
python -m pytest -q
```

The tests check API examples and bookkeeping; they do not establish experimental validation of material failure rates.

## Research, citation, and license

Authors: Ugwiyeon Lee, Seong-Yun Bae, Hakrae Kim, Jungsu Lee, and Jinseo Kim.  
Affiliation: Gas Safety R&D Institute, Korea Gas Safety Corporation.  
Contact: [lyullee@kgs.or.kr](mailto:lyullee@kgs.or.kr).

Release DOI: [10.5281/zenodo.23550690](https://doi.org/10.5281/zenodo.23550690). Use the versioned record and repository citation metadata when citing a calculation.

Funding: This work was supported by the Korea Institute of Energy Technology Evaluation and Planning (KETEP), funded by the Korea government (Ministry of Climate, Energy and Environment) [grant number RS-2024-00437207]. The funder had no role in study design, data collection, analysis or interpretation, manuscript preparation, or the decision to submit the article.

Distributed under the [MIT License](LICENSE).
