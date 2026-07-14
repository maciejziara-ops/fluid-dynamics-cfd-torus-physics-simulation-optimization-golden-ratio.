import math


def golden_ratio():
    """Zwraca wartość liczby Phi (Złoty Podział)."""
    return (1 + math.sqrt(5)) / 2.0


import math
from typing import Dict


def golden_ratio() -> float:
    """Zwraca wartość liczby Phi (Złoty Podział)."""
    return (1 + math.sqrt(5)) / 2.0


def golden_geometry() -> Dict[str, float]:
    """Definiuje geometrię torusa opartą na kwadracie liczby Phi."""
    phi = golden_ratio()
    phi_squared = phi ** 2
    return {
        "aspect_ratio": phi_squared,
        "helical_path_factor": phi_squared,
    }


def _compute_stability_score(reynolds_number: float) -> float:
    """Prosty heurystyczny wskaźnik stabilności w zakresie [0, 1].

    Wyższa wartość oznacza większą stabilność (mniej turbulencji).
    Implementacja jest heurystyczna: zmniejsza się wraz ze wzrostem Re.
    """
    if reynolds_number <= 0:
        raise ValueError("reynolds_number must be positive")

    # Logistic-like spadek stabilności wobec rosnącego Re.
    # Parametry dobrane tak, aby:
    # - Re ~ 1000 -> score blisko 0.8-0.95 (laminar)
    # - Re ~ 2300 -> score ~ 0.6 (granica przejścia)
    # - Re ~ 5000 -> score ~ 0.3-0.4 (turbulent)
    ratio = reynolds_number / 3000.0
    score = 1.0 / (1.0 + ratio ** 1.2)
    # zabezpieczenie przed numerycznymi skokami
    return max(0.0, min(1.0, float(score)))


def optimize_torus_geometry(reynolds_number: float) -> Dict[str, float]:
    """
    Optymalizuje parametry torusa dla danego przepływu.
    Zwraca geometrię i ocenę stabilności zależną od liczby Reynoldsa.
    """
    phi = golden_ratio()
    if reynolds_number is None:
        raise ValueError("reynolds_number is required")

    # Kąt w stopniach obliczony z arctan(1/phi)
    # Wynik to około 31.72 stopnia
    angle_deg = math.degrees(math.atan(1 / phi))
    stability = _compute_stability_score(float(reynolds_number))
    return {
        "aspect_ratio": phi ** 2,
        "injection_angle_deg": angle_deg,
        "stability_score": stability,
    }
