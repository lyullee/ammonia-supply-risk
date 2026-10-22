from ammonia_supply_risk import conditional_risk, material_screening, mutually_exclusive_paths


def test_material_screening_contains_mandatory_grades():
    names = {row["material"] for row in material_screening(n_samples=1_000)}
    assert {"STS304", "STS316L", "STS317"} <= names


def test_frequency_multiplier():
    assert conditional_risk(1.0, 2.0, 3.0) == 6.0


def test_paths_allocate_once():
    assert mutually_exclusive_paths(10.0, [0.2, 0.8]) == [2.0, 8.0]
