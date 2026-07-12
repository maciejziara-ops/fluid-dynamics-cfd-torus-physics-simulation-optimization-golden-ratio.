import math
from typing import Dict


def golden_ratio() -> float:
    """Return the golden ratio constant phi."""
    return (1 + math.sqrt(5)) / 2.0


def golden_geometry() -> Dict[str, float]:
    """Define a toroidal geometry aligned with phi^2."""
    phi = golden_ratio()
    return {
        "aspect_ratio": phi**2,
        "helical_path_factor": phi**2,
        "injection_angle_deg": math.degrees(math.atan(1 / phi)),
    }


def optimize_torus_geometry(reynolds_number: float) -> Dict[str, float]:
    """Estimate a stable toroidal geometry for a given Reynolds number."""
    geom = golden_geometry()
    stability_score = 1.0 / (1.0 + reynolds_number / 10000.0)
    return {
        "aspect_ratio": geom["aspect_ratio"],
        "helical_path_factor": geom["helical_path_factor"],
        "injection_angle_deg": geom["injection_angle_deg"],
        "stability_score": stability_score,
        "recommended_flow_regime": "laminar-stable" if stability_score < 0.5 else "transitional",
    }
