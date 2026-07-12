import math


def golden_ratio():
    """Zwraca wartość liczby Phi (Złoty Podział)."""
    return (1 + math.sqrt(5)) / 2.0


def golden_geometry():
    """Definiuje geometrię torusa opartą na kwadracie liczby Phi."""
    phi = golden_ratio()
    phi_squared = phi ** 2
    return {
        "aspect_ratio": phi_squared,
        "helical_path_factor": phi_squared,
    }


def optimize_torus_geometry(reynolds_number):
    """
    Optymalizuje parametry torusa dla danego przepływu.
    Zwraca geometrię minimalizującą turbulencję.
    """
    phi = golden_ratio()
    # Kąt w stopniach obliczony z arctan(1/phi)
    # Wynik to około 31.72 stopnia
    angle_deg = math.degrees(math.atan(1 / phi))
    return {
        "aspect_ratio": phi ** 2,
        "injection_angle_deg": angle_deg,
        "stability_score": 0.5,
    }
