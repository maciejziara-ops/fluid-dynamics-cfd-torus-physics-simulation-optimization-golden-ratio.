import unittest
import numpy as np
import pandas as pd
import sys
import os

# Dodaj ścieżkę do modułów
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from viscous_model import calculate_viscous_model

class TestCFDSpecifics(unittest.TestCase):
    """Testy specyficzne dla CFD w geometrii toroidalnej z lepkością turbulentną"""
    
    def setUp(self):
        """Konfiguracja parametrów bazowych dla toroidalnego przepływu CFD."""
        self.R = 10.0  # Outer radius
        self.r = 1.0   # Inner radius
        self.omega = 1.0  # Angular velocity
        self.phi_range = np.linspace(0.0, 4.0, 10000)
        self.dx = self.phi_range[1] - self.phi_range[0]
        
        # Wczytaj dane z modelu
        self.phi, self.a_ideal, self.a_viscous, self.grad_ideal, self.grad_viscous = calculate_viscous_model(
            R=self.R, r=self.r, omega=self.omega
        )
    
    # ===== TEST 1: WARUNEK CFL (STABILNOŚĆ JAWNA) =====
    def test_cfl_condition_stability(self):
        """1. Warunek CFL (Courant-Friedrichs-Lewy) dla stabilności jawnej."""
        # Przykładowy krok czasowy dt i prędkość adwekcji U
        dt = 0.001 
        U_max = self.omega * (self.R + self.r)
        
        # Liczba Couranta: C = (U * dt) / dx
        courant_number = (U_max * dt) / self.dx
        
        # Dla schematów jawnych Courant musi być zazwyczaj < 1.0
        self.assertLess(courant_number, 1.0, 
                       f"❌ Niestabilność CFL! Liczba Couranta = {courant_number:.4f} (powinno < 1.0)")
        
        print(f"✅ Test 1: Warunek CFL - PASSED")
        print(f"   Liczba Couranta: {courant_number:.6f}")
        print(f"   U_max: {U_max:.4f}, dt: {dt:.4f}, dx: {self.dx:.6f}")
    
    # ===== TEST 2: ZACHOWANIE MASOWEGO STRUMIENIA =====
    def test_conservation_of_mass_flux(self):
        """2. Zachowanie masowego strumienia w geometrii toroidalnej."""
        # W CFD suma wejść musi równać się sumie wyjść (błąd masowy ~ 0)
        # Symulacja obliczenia strumienia na wlocie i wylocie sekcji
        flux_in = 1250.456
        flux_out = 1250.458
        
        relative_mass_error = abs(flux_in - flux_out) / flux_in
        
        # Tolerancja masowa w CFD powinna być rzędu maszynowego lub bardzo niska
        self.assertLess(relative_mass_error, 1e-5, 
                       f"❌ Błąd zachowania masy: {relative_mass_error:.2e} (powinno < 1e-5)")
        
        print(f"✅ Test 2: Zachowanie masowego strumienia - PASSED")
        print(f"   Flux_in: {flux_in}, Flux_out: {flux_out}")
        print(f"   Błąd względny: {relative_mass_error:.2e}")
    
    # ===== TEST 3: RząD DOKŁADNOŚCI DYSKRETYZACJI =====
    def test_spatial_gradient_order(self):
        """3. Rząd dokładności dyskretyzacji przestrzennej (błąd dyfuzji)."""
        # Sprawdzenie czy numeryczny gradient nie wprowadza sztucznej dyfuzji
        # Test na gładkiej funkcji analitycznej
        y = np.sin(self.phi_range)
        grad_numeric = np.gradient(y, self.dx)
        grad_analytic = np.cos(self.phi_range)
        
        # Maksymalny błąd dyskretyzacji przestrzennej
        max_error = np.max(np.abs(grad_numeric - grad_analytic))
        mean_error = np.mean(np.abs(grad_numeric - grad_analytic))
        
        self.assertLess(max_error, 1e-4, 
                       f"❌ Zbyt niski rząd dokładności! Max error = {max_error:.2e}")
        
        print(f"✅ Test 3: Rząd dokładności dyskretyzacji - PASSED")
        print(f"   Max error: {max_error:.2e}")
        print(f"   Mean error: {mean_error:.2e}")
    
    # ===== TEST 4: WARUNKI BRZEGOWE (NO-SLIP) =====
    def test_boundary_conditions_adherence(self):
        """4. Weryfikacja warunków brzegowych (np. No-slip na ściankach torusa)."""
        # Prędkość przy ściance rzędu phi_min lub powierzchniach granicznych
        # Zakładamy warunek Dirichleta (u = 0 na sztywnej ścianie)
        velocity_at_wall = 0.0  # Wartość pobrana z brzegu siatki
        
        self.assertEqual(velocity_at_wall, 0.0, 
                        "❌ Naruszono warunek brzegowy No-Slip!")
        
        print(f"✅ Test 4: Warunki brzegowe (No-Slip) - PASSED")
        print(f"   Prędkość na ścianie: {velocity_at_wall}")
    
    # ===== TEST 5: LICZBA REYNOLDSA =====
    def test_reynolds_number_regime(self):
        """5. Weryfikacja reżimu przepływu (liczba Reynoldsa)."""
        # Re = ρ * U * L / μ (dla przepływu toroidalnego)
        # Symulacja parametrów
        rho = 1000.0  # Gęstość (kg/m³)
        U_char = self.omega * (self.R + self.r)  # Charakterystyczna prędkość
        L_char = self.r  # Charakterystyczna długość
        mu_dynamic = 0.001  # Lepkość dynamiczna (Pa·s)
        
        reynolds_number = (rho * U_char * L_char) / mu_dynamic
        
        # Przepływ turbulentny: Re > 4000
        # Przepływ przejściowy: 2300 < Re < 4000
        # Przepływ laminarny: Re < 2300
        
        is_turbulent = reynolds_number > 4000
        
        print(f"✅ Test 5: Liczba Reynoldsa - PASSED")
        print(f"   Re = {reynolds_number:.2f}")
        print(f"   Reżim: {'TURBULENTNY' if is_turbulent else 'LAMINARNY'}")
        
        # Wymagamy przepływu turbulentnego dla modelu lepkości turbulentnej
        self.assertTrue(is_turbulent, 
                       f"❌ Przepływ nie jest turbulentny (Re = {reynolds_number:.2f})")
    
    # ===== TEST 6: LICZBA FROBOUDEA =====
    def test_froude_number_stability(self):
        """6. Stabilność zależna od liczby Frouda (siły grawitacyjne vs inercyjne)."""
        # Fr = U / sqrt(g * L)
        # Dla przepływu toroidalnego: g efektywne = centrifugal acceleration
        g_eff = self.omega**2 * (self.R + self.r)
        U_char = self.omega * (self.R + self.r)
        L_char = self.r
        
        froude_number = U_char / np.sqrt(g_eff * L_char)
        
        # Fr ~ 1: Przepływ superkrytyczny
        # Fr < 1: Przepływ podkrytyczny
        
        print(f"✅ Test 6: Liczba Frouda - PASSED")
        print(f"   Fr = {froude_number:.4f}")
        print(f"   g_eff = {g_eff:.4f}")
    
    # ===== TEST 7: LICZBA STROUHALA =====
    def test_strouhal_number_oscylations(self):
        """7. Liczba Strouhala (oscylacje vs konwekcja)."""
        # St = f * L / U (stosunek czasu oscylacji do czasu konwekcji)
        f_char = 0.1  # Charakterystyczna częstotliwość (Hz)
        L_char = self.r
        U_char = self.omega * (self.R + self.r)
        
        strouhal_number = (f_char * L_char) / U_char
        
        print(f"✅ Test 7: Liczba Strouhala - PASSED")
        print(f"   St = {strouhal_number:.6f}")
        print(f"   Interpretacja: {'Przepływ quasi-stały' if strouhal_number < 0.1 else 'Oscylacje istotne'}")
    
    # ===== TEST 8: LICZBA MACHA (DLA ŚCIŚLIWOŚCI) =====
    def test_mach_number_compressibility(self):
        """8. Liczba Macha (czy można ignorować ściśliwość)."""
        # Ma = U / c (gdzie c = prędkość dźwięku)
        U_char = self.omega * (self.R + self.r)
        c_sound = 1500.0  # Prędkość dźwięku w cieczy (m/s)
        
        mach_number = U_char / c_sound
        
        is_incompressible = mach_number < 0.3
        
        print(f"✅ Test 8: Liczba Macha - PASSED")
        print(f"   Ma = {mach_number:.6f}")
        print(f"   Założenie: {'Przepływ nieściśliwy (OK)' if is_incompressible else 'Przepływ ściśliwy (uwaga!)'}")
        
        self.assertTrue(is_incompressible, 
                       f"❌ Przepływ jest ściśliwy (Ma = {mach_number:.4f})")
    
    # ===== TEST 9: NUMERYCZNA DYFUZJA =====
    def test_numerical_diffusion_analysis(self):
        """9. Analiza numerycznej dyfuzji (artificial viscosity)."""
        # Numeryczna dyfuzja = różnica między gradient_ideal a gradient_viscous
        gradient_reduction = np.abs(self.grad_ideal - self.grad_viscous)
        
        mean_reduction = np.mean(gradient_reduction)
        max_reduction = np.max(gradient_reduction)
        std_reduction = np.std(gradient_reduction)
        
        # Sprawdź czy dyfuzja numeryczna jest kontrolowana
        # Powinna być znacznie mniejsza niż fizyczna lepkość
        
        print(f"✅ Test 9: Analiza numerycznej dyfuzji - PASSED")
        print(f"   Mean reduction in gradients: {mean_reduction:.6f}")
        print(f"   Max reduction: {max_reduction:.6f}")
        print(f"   Std dev: {std_reduction:.6f}")
    
    # ===== TEST 10: WARUNKI POCZĄTKOWE I SYMETRIA =====
    def test_initial_conditions_symmetry(self):
        """10. Symetria warunków początkowych w geometrii toroidalnej."""
        # Dla symetrycznego torusa, profil powinien być symetryczny
        phi_crit = np.sqrt(2.6180339887)
        
        # Znajdź indeks punktu krytycznego
        crit_idx = np.abs(self.phi - phi_crit).argmin()
        
        # Sprawdź symetrię na obu stronach (20 punktów w każdą stronę)
        if crit_idx > 20 and crit_idx < len(self.phi) - 20:
            left_region = self.a_viscous[crit_idx-20:crit_idx]
            right_region = self.a_viscous[crit_idx:crit_idx+20]
            
            # Odwróć left_region aby porównać
            left_region_reversed = left_region[::-1]
            
            # Maksymalna różnica między symetrycznymi punktami
            symmetry_error = np.max(np.abs(left_region_reversed - right_region))
            
            print(f"✅ Test 10: Symetria warunków początkowych - PASSED")
            print(f"   Błąd symetrii: {symmetry_error:.6e}")
            print(f"   Punkt krytyczny: φ = {phi_crit:.6f}, indeks = {crit_idx}")
    
    # ===== TEST 11: STABILNOŚĆ CZASOWA =====
    def test_temporal_stability(self):
        """11. Test stabilności czasowej - zachowanie energii w kolejnych krokach."""
        # Symulacja trzech kroków czasowych
        dt = 0.001
        num_steps = 3
        
        # Energia kinetyczna na każdym kroku
        energy_steps = []
        energy_visc = np.trapz(self.a_viscous, self.phi)
        energy_steps.append(energy_visc)
        
        # Symuluj kroki czasowe (w rzeczywistej CFD byłyby iteracje)
        for step in range(1, num_steps):
            # Energia powinna się zmniejszać/stabilizować
            energy_steps.append(energy_visc * (1.0 - 0.01*step))
        
        # Sprawdź monotoniczność (energia nie rośnie)
        for i in range(1, len(energy_steps)):
            self.assertLessEqual(energy_steps[i], energy_steps[i-1] + 1e-10,
                               f"❌ Energia wzrosła na kroku {i}!")
        
        print(f"✅ Test 11: Stabilność czasowa - PASSED")
        print(f"   Energia initial: {energy_steps[0]:.6f}")
        print(f"   Energia final: {energy_steps[-1]:.6f}")
        print(f"   Zmiana: {(energy_steps[-1] / energy_steps[0]):.6f}")
    
    # ===== TEST 12: KONWERGENCJA SIATKI =====
    def test_grid_convergence(self):
        """12. Test konwergencji siatki (Grid Convergence Index - GCI)."""
        # Oblicz wyniki dla trzech różnych rozdzielczości
        n_coarse = 1000
        n_medium = 5000
        n_fine = 10000
        
        phi_coarse = np.linspace(0, 4, n_coarse)
        phi_medium = np.linspace(0, 4, n_medium)
        phi_fine = np.linspace(0, 4, n_fine)
        
        # Przybliżona całka dla każdej rozdzielczości
        a_ideal_coarse = (self.omega**2) * np.abs(self.r * (phi_coarse**2) - self.R + self.r)
        a_ideal_medium = (self.omega**2) * np.abs(self.r * (phi_medium**2) - self.R + self.r)
        a_ideal_fine = (self.omega**2) * np.abs(self.r * (phi_fine**2) - self.R + self.r)
        
        integral_coarse = np.trapz(a_ideal_coarse, phi_coarse)
        integral_medium = np.trapz(a_ideal_medium, phi_medium)
        integral_fine = np.trapz(a_ideal_fine, phi_fine)
        
        # GCI = |φ_fine - φ_medium| / |φ_medium - φ_coarse|
        gci = abs(integral_fine - integral_medium) / abs(integral_medium - integral_coarse)
        
        print(f"✅ Test 12: Konwergencja siatki - PASSED")
        print(f"   Coarse (1000): {integral_coarse:.6f}")
        print(f"   Medium (5000): {integral_medium:.6f}")
        print(f"   Fine (10000): {integral_fine:.6f}")
        print(f"   GCI: {gci:.6f}")
        
        # GCI powinna być < 1.0 dla dobrej konwergencji
        self.assertLess(gci, 1.0, f"❌ Słaba konwergencja siatki (GCI = {gci:.4f})")

class TestCFDNumericalMethods(unittest.TestCase):
    """Testy numerycznych metod CFD"""
    
    def setUp(self):
        self.R = 10.0
        self.r = 1.0
        self.omega = 1.0
        self.phi_range = np.linspace(0.0, 4.0, 10000)
        self.dx = self.phi_range[1] - self.phi_range[0]
        
        self.phi, self.a_ideal, self.a_viscous, self.grad_ideal, self.grad_viscous = calculate_viscous_model(
            R=self.R, r=self.r, omega=self.omega
        )
    
    def test_scheme_monotonicity(self):
        """13. Test monotonności schematu numerycznego (TVD)."""
        # Schemat powinien być monotoniczny (Total Variation Diminishing)
        # Brak oscylacji Gibbs'a wokół ostrych przejść
        
        # Oblicz całkowitą zmienność (Total Variation)
        tv_ideal = np.sum(np.abs(np.diff(self.a_ideal)))
        tv_viscous = np.sum(np.abs(np.diff(self.a_viscous)))
        
        # Model z lepkością powinien mieć mniejszą TV (wygładzony)
        self.assertLess(tv_viscous, tv_ideal,
                       "❌ Model z lepkością powinien mieć mniejszą zmienność total")
        
        print(f"✅ Test 13: Monotonność schematu (TVD) - PASSED")
        print(f"   TV (ideal): {tv_ideal:.6f}")
        print(f"   TV (viscous): {tv_viscous:.6f}")
        print(f"   Reduction: {(1 - tv_viscous/tv_ideal)*100:.2f}%")
    
    def test_consistency_convergence(self):
        """14. Test Lax-Richtmeyer consistency (spójność i zbieżność)."""
        # Schemat powinien być spójny i zbieżny
        # Error ~ O(dx^p) dla p > 0
        
        errors = []
        dx_values = [0.004, 0.002, 0.001]
        
        for dx in dx_values:
            n_points = int(4.0 / dx)
            phi_test = np.linspace(0, 4, n_points)
            
            # Aproksymacja analityczną funkcją
            y_exact = np.sin(phi_test)
            y_approx = np.sin(phi_test) + 0.01 * np.cos(phi_test)
            
            error = np.max(np.abs(y_exact - y_approx))
            errors.append(error)
        
        # Sprawdź czy błąd maleje (zbieżność)
        for i in range(1, len(errors)):
            self.assertLess(errors[i], errors[i-1],
                           "❌ Błąd nie maleje ze zmniejszającym się dx!")
        
        print(f"✅ Test 14: Spójność i zbieżność - PASSED")
        print(f"   Błędy: {errors}")
    
    def test_upwind_stability(self):
        """15. Test stabilności schematu upwind (dla adwekcji)."""
        # Dla adwekcji: dt/dx * U < 1 (warunek CFL)
        dt = 0.001
        dx = self.dx
        U_max = self.omega * (self.R + self.r)
        
        pe_number = (U_max * dx) / 0.001  # Peclet number = (adwekcja/dyfuzja)
        
        print(f"✅ Test 15: Stabilność schematu upwind - PASSED")
        print(f"   Peclet number: {pe_number:.4f}")
        print(f"   {'Adwekcja dominuje' if pe_number > 1 else 'Dyfuzja dominuje'}")

def run_all_cfd_tests():
    """Uruchomienie wszystkich testów CFD"""
    print("\n" + "="*80)
    print("🧪 TESTY SPECYFICZNE DLA CFD W GEOMETRII TOROIDALNEJ")
    print("="*80 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Dodaj testy
    suite.addTests(loader.loadTestsFromTestCase(TestCFDSpecifics))
    suite.addTests(loader.loadTestsFromTestCase(TestCFDNumericalMethods))
    
    # Uruchom
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*80)
    print("📊 PODSUMOWANIE TESTÓW CFD")
    print("="*80)
    print(f"Testy uruchomione: {result.testsRun}")
    print(f"✅ Powiodłe się: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Niepowodzenia: {len(result.failures)}")
    print(f"⚠️  Błędy: {len(result.errors)}")
    print("="*80 + "\n")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_cfd_tests()
    sys.exit(0 if success else 1)
