import math

from toroidal_flow import (
    golden_ratio,
    golden_geometry,
    optimize_torus_geometry,
)


def test_golden_ratio_matches_expected_value():
    phi = golden_ratio()
    assert math.isclose(phi, 1.618033988749895, rel_tol=1e-12)


def test_golden_geometry_uses_phi_squared_aspect_ratio():
    params = golden_geometry()
    assert math.isclose(params["aspect_ratio"], golden_ratio() ** 2, rel_tol=1e-12)
    assert math.isclose(params["helical_path_factor"], golden_ratio() ** 2, rel_tol=1e-12)


def test_optimization_prefers_phi_aligned_geometry():
    result = optimize_torus_geometry(reynolds_number=5000)
    assert result["aspect_ratio"] > 2.0
    assert result["injection_angle_deg"] > 20.0
    assert result["injection_angle_deg"] < 40.0
    assert result["stability_score"] < 1.0
