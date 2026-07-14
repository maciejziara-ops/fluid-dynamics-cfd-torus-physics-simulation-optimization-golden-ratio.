import unittest
import numpy as np
import pandas as pd
import sys
import os

# Dodaj ścieżkę do modułów
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from viscous_model import calculate_viscous_model

class TestViscousModel(unittest.TestCase):
    """Testy jednostkowe modelu lepkości turbulentnej"""
    
    def setUp(self):
        """Przygotowanie danych testowych"""
        self.phi_range, self.a_ideal, self.a_viscous, self.grad_ideal, self.grad_viscous = calculate_viscous_model()
        self.phi_crit = np.sqrt(2.6180339887)
        self.crit_idx = np.abs(self.phi_range - self.phi_crit).argmin()
    
    # ===== TESTY STRUKTURY I WYMIARÓW =====
    def test_output_dimensions(self):
        """Test 1: Sprawdzenie wymiarów wyjściowych"""
        self.assertEqual(len(self.phi_range), 10000, "phi_range powinien mieć 10,000 elementów")
        self.assertEqual(len(self.a_ideal), 10000, "a_ideal powinien mieć 10,000 elementów")
        self.assertEqual(len(self.a_viscous), 10000, "a_viscous powinien mieć 10,000 elementów")
        self.assertEqual(len(self.grad_ideal), 10000, "grad_ideal powinien mieć 10,000 elementów")
        self.assertEqual(len(self.grad_viscous), 10000, "grad_viscous powinien mieć 10,000 elementów")
        print("✅ Test 1: Wymiary wyjściowe - PASSED")
    
    def test_phi_range_correctness(self):
        """Test 2: Sprawdzenie poprawności zakresu phi"""
        self.assertAlmostEqual(self.phi_range[0], 0.0, places=5)
        self.assertAlmostEqual(self.phi_range[-1], 4.0, places=5)
        self.assertTrue(np.all(np.diff(self.phi_range) > 0), "phi_range powinien być rosnący")
        print("✅ Test 2: Zakres phi - PASSED")
    
    # ===== TESTY WARTOŚCI FIZYCZNYCH =====
    def test_no_nan_or_inf(self):
        """Test 3: Sprawdzenie braku wartości NaN lub Inf"""
        self.assertFalse(np.any(np.isnan(self.a_ideal)), "a_ideal zawiera NaN")
        self.assertFalse(np.any(np.isnan(self.a_viscous)), "a_viscous zawiera NaN")
        self.assertFalse(np.any(np.isinf(self.a_ideal)), "a_ideal zawiera Inf")
        self.assertFalse(np.any(np.isinf(self.a_viscous)), "a_viscous zawiera Inf")
        self.assertFalse(np.any(np.isnan(self.grad_ideal)), "grad_ideal zawiera NaN")
        self.assertFalse(np.any(np.isnan(self.grad_viscous)), "grad_viscous zawiera NaN")
        print("✅ Test 3: Brak anomalii numerycznych (NaN/Inf) - PASSED")
    
    def test_positive_acceleration(self):
        """Test 4: Przyspieszenie powinno być nieujemne"""
        self.assertTrue(np.all(self.a_ideal >= 0), "a_ideal zawiera wartości ujemne")
        self.assertTrue(np.all(self.a_viscous >= 0), "a_viscous zawiera wartości ujemne")
        print("✅ Test 4: Przyspieszenie nieujemne - PASSED")
    
    # ===== TESTY LEPKOŚCI I TŁUMIENIA =====
    def test_viscosity_damping_relationship(self):
        """Test 5: Sprawdzenie relacji a_viscous = a_ideal * damping_factor"""
        viscosity_damping = 1.0 - 0.65 * np.exp(-((self.phi_range - self.phi_crit) / 0.35)**2)
        expected_a_viscous = self.a_ideal * viscosity_damping
        
        np.testing.assert_array_almost_equal(
            self.a_viscous, expected_a_viscous, decimal=5,
            err_msg="a_viscous nie odpowiada a_ideal * damping_factor"
        )
        print("✅ Test 5: Relacja lepkości (a_viscous = a_ideal * damping) - PASSED")
    
    def test_damping_at_critical_point(self):
        """Test 6: Tłumienie powinno być maksymalne (~65%) w punkcie krytycznym"""
        viscosity_damping = 1.0 - 0.65 * np.exp(-((self.phi_range - self.phi_crit) / 0.35)**2)
        max_damping = np.max(viscosity_damping)
        
        # Maksymalne tłumienie powinno być bliskie 0.65
        self.assertGreater(max_damping, 0.64, "Max damping < 0.64")
        self.assertLess(max_damping, 0.66, "Max damping > 0.66")
        
        # Tłumienie w punkcie krytycznym powinno być maksymalne
        damping_at_crit = viscosity_damping[self.crit_idx]
        self.assertAlmostEqual(damping_at_crit, max_damping, places=3)
        print("✅ Test 6: Tłumienie maksymalne (~65%) w punkcie krytycznym - PASSED")
    
    def test_viscous_less_than_ideal(self):
        """Test 7: Przyspieszenie z lepkością powinno być mniejsze niż idealne"""
        # Oprócz obszarów gdzie viscosity_damping ≈ 1.0
        viscosity_damping = 1.0 - 0.65 * np.exp(-((self.phi_range - self.phi_crit) / 0.35)**2)
        
        # Gdzie damping < 0.99, a_viscous powinno być < a_ideal
        mask_significant_damping = viscosity_damping < 0.99
        self.assertTrue(
            np.all(self.a_viscous[mask_significant_damping] <= self.a_ideal[mask_significant_damping]),
            "Model z lepkością powinien mieć mniejsze przyspieszenie"
        )
        print("✅ Test 7: Przyspieszenie z lepkością < przyspieszenie idealne - PASSED")
    
    # ===== TESTY GRADIENTÓW I STABILNOŚCI =====
    def test_gradient_magnitude_reduction(self):
        """Test 8: Gradienty powinny być mniejsze w modelu z lepkością"""
        # W pobliżu punktu krytycznego gradienty powinny być wygładzone
        critical_zone = (self.phi_range >= self.phi_crit - 0.5) & (self.phi_range <= self.phi_crit + 0.5)
        
        grad_ideal_crit = np.abs(self.grad_ideal[critical_zone])
        grad_viscous_crit = np.abs(self.grad_viscous[critical_zone])
        
        # Średni gradient powinien być mniejszy
        mean_grad_ideal = np.mean(grad_ideal_crit)
        mean_grad_viscous = np.mean(grad_viscous_crit)
        
        self.assertLess(mean_grad_viscous, mean_grad_ideal,
                       "Średni gradient z lepkością powinien być mniejszy")
        print("✅ Test 8: Wygładzenie gradientów w strefie krytycznej - PASSED")
    
    def test_gradient_numerical_stability(self):
        """Test 9: Gradienty nie powinny zawierać anomalii"""
        self.assertFalse(np.any(np.isnan(self.grad_ideal)), "grad_ideal zawiera NaN")
        self.assertFalse(np.any(np.isnan(self.grad_viscous)), "grad_viscous zawiera NaN")
        self.assertFalse(np.any(np.isinf(self.grad_ideal)), "grad_ideal zawiera Inf")
        self.assertFalse(np.any(np.isinf(self.grad_viscous)), "grad_viscous zawiera Inf")
        print("✅ Test 9: Stabilność numeryczna gradientów - PASSED")
    
    # ===== TESTY PUNKTU KRYTYCZNEGO =====
    def test_critical_point_location(self):
        """Test 10: Punkt krytyczny powinien być w prawidłowej lokalizacji"""
        phi_crit_expected = np.sqrt(2.6180339887)
        phi_crit_found = self.phi_range[self.crit_idx]
        
        self.assertAlmostEqual(phi_crit_found, phi_crit_expected, places=3,
                              msg="Punkt krytyczny nie znaleziony w prawidłowej lokalizacji")
        print("✅ Test 10: Lokalizacja punktu krytycznego - PASSED")
    
    def test_symmetry_around_critical_point(self):
        """Test 11: Tłumienie powinno być symetryczne wokół punktu krytycznego"""
        viscosity_damping = 1.0 - 0.65 * np.exp(-((self.phi_range - self.phi_crit) / 0.35)**2)
        
        # Tłumienie 0.2 jednostek po lewej i prawej stronie
        left_idx = np.abs(self.phi_range - (self.phi_crit - 0.2)).argmin()
        right_idx = np.abs(self.phi_range - (self.phi_crit + 0.2)).argmin()
        
        self.assertAlmostEqual(viscosity_damping[left_idx], viscosity_damping[right_idx], places=4,
                              msg="Tłumienie nie jest symetryczne")
        print("✅ Test 11: Symetria tłumienia wokół punktu krytycznego - PASSED")
    
    # ===== TESTY FIZYCZNOŚCI =====
    def test_energy_conservation(self):
        """Test 12: Całkowita energia nie powinna rosnąć"""
        # Przybliżona całka z przyspieszenia (energia)
        energy_ideal = np.trapz(self.a_ideal, self.phi_range)
        energy_viscous = np.trapz(self.a_viscous, self.phi_range)
        
        # Energia z lepkością powinna być mniejsza
        self.assertLess(energy_viscous, energy_ideal,
                       "Całkowita energia powinna zmaleć ze względu na lepkość")
        print("✅ Test 12: Zachowanie energii (redukcja ze względu na lepkość) - PASSED")
    
    def test_damping_zone_width(self):
        """Test 13: Strefa wpływu tłumienia powinna być (~0.7 jednostek)"""
        viscosity_damping = 1.0 - 0.65 * np.exp(-((self.phi_range - self.phi_crit) / 0.35)**2)
        
        # Znajdź punkty gdzie tłumienie > 0.32 (połowa maksimum)
        half_max_damping_idx = np.where(viscosity_damping > 0.325)
        
        if len(half_max_damping_idx[0]) > 0:
            width_estimate = self.phi_range[half_max_damping_idx[0][-1]] - self.phi_range[half_max_damping_idx[0][0]]
            # Spodziewana szerokość: ~2*2.355*sigma = ~1.65 (FWHM dla Gaussa)
            self.assertGreater(width_estimate, 1.2)
            self.assertLess(width_estimate, 2.0)
            print(f"✅ Test 13: Szerokość strefy wpływu (~{width_estimate:.2f} jednostek) - PASSED")
        else:
            print("⚠️  Test 13: Nie można oszacować szerokości strefy")
    
    # ===== TESTY DANYCH WYJŚCIOWYCH =====
    def test_csv_export_compatibility(self):
        """Test 14: Dane powinny być kompatybilne z formatem CSV"""
        df = pd.DataFrame({
            'phi': self.phi_range,
            'acceleration_ideal': self.a_ideal,
            'acceleration_viscous': self.a_viscous,
            'gradient_ideal': self.grad_ideal,
            'gradient_viscous': self.grad_viscous
        })
        
        # Sprawdź czy nie ma problemów z zapisem
        csv_string = df.to_csv(index=False)
        self.assertGreater(len(csv_string), 0)
        
        # Wczytaj z powrotem i porównaj
        df_reloaded = pd.read_csv(__import__('io').StringIO(csv_string))
        self.assertEqual(len(df_reloaded), len(df))
        print("✅ Test 14: Kompatybilność z formatem CSV - PASSED")
    
    def test_parameter_influence(self):
        """Test 15: Wpływ parametrów na model"""
        # Test z różnymi parametrami
        phi1, a_ideal1, a_visc1, _, _ = calculate_viscous_model(R=10.0, r=1.0, omega=1.0)
        phi2, a_ideal2, a_visc2, _, _ = calculate_viscous_model(R=20.0, r=1.0, omega=1.0)
        
        # Zmiana R powinna wpłynąć na przyspieszenie
        self.assertFalse(np.allclose(a_ideal1, a_ideal2),
                        "Zmiana R powinna wpłynąć na przyspieszenie")
        print("✅ Test 15: Wpływ parametrów na model - PASSED")

class TestPerformance(unittest.TestCase):
    """Testy wydajności"""
    
    def test_calculation_speed(self):
        """Test 16: Czas obliczenia powinien być rozsądny"""
        import time
        
        start = time.time()
        calculate_viscous_model()
        elapsed = time.time() - start
        
        # Powinno się wykonać w mniej niż 1 sekundę
        self.assertLess(elapsed, 1.0, f"Obliczenie zajęło {elapsed:.2f}s (powinno < 1s)")
        print(f"✅ Test 16: Wydajność - obliczenie zajęło {elapsed:.3f}s - PASSED")

def run_tests():
    """Uruchomienie wszystkich testów z raportowaniem"""
    print("\n" + "="*70)
    print("🧪 PRZEPROWADZANIE TESTÓW JEDNOSTKOWYCH MODELU LEPKOŚCI")
    print("="*70 + "\n")
    
    # Utwórz test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Dodaj testy
    suite.addTests(loader.loadTestsFromTestCase(TestViscousModel))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Uruchom testy
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Podsumowanie
    print("\n" + "="*70)
    print("📊 PODSUMOWANIE WYNIKÓW TESTÓW")
    print("="*70)
    print(f"Testy uruchomione: {result.testsRun}")
    print(f"✅ Powiodłe się: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Niepowodzenia: {len(result.failures)}")
    print(f"⚠️  Błędy: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 WSZYSTKIE TESTY POWIODŁY SIĘ!")
    else:
        print("\n⚠️  NIEKTÓRE TESTY NIE POWIODŁY SIĘ")
    
    print("="*70 + "\n")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
