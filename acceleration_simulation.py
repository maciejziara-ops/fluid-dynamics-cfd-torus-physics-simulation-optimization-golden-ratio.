import csv
import math
import matplotlib.pyplot as plt

def check_equation(R, r, phi_list, omega=1.0):
    results = []
    for phi in phi_list:
        # Twój wzór na przyspieszenie
        a = (omega**2) * abs(r * (phi**2) - R + r)
        results.append((phi, a))
    return results

def save_results_to_csv(results, filename='acceleration_results.csv'):
    """Save acceleration results to a CSV file."""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['phi', 'acceleration'])  # Header row
        for phi, acceleration in results:
            writer.writerow([phi, acceleration])
    print(f"Results saved to {filename}")

def plot_results(results, title="Acceleration vs Phi", filename='acceleration_plot.png'):
    """Create and save a scatter plot of the results."""
    phi_values = [r[0] for r in results]
    acceleration_values = [r[1] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(phi_values, acceleration_values, color='red', s=100, alpha=0.7, edgecolors='black', linewidth=1.5)
    plt.plot(phi_values, acceleration_values, color='blue', alpha=0.5, linestyle='--', label='Trend')
    
    # Highlight the critical point at phi ≈ 2.618
    critical_phi = 2.618
    critical_a = (1.0**2) * abs(1 * (critical_phi**2) - 10 + 1)
    plt.scatter([critical_phi], [critical_a], color='green', s=200, marker='*', 
                edgecolors='darkgreen', linewidth=2, label=f'Critical Point (φ={critical_phi})', zorder=5)
    
    plt.xlabel('Phi (φ)', fontsize=12, fontweight='bold')
    plt.ylabel('Acceleration (a)', fontsize=12, fontweight='bold')
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {filename}")
    plt.show()

# Parametry
R_test = 10
r_test = 1

# Test 1: Original sample list
print("=" * 60)
print("TEST 1: Oryginalna lista próbek")
print("=" * 60)
phi_test_original = [1.0, 1.5, 2.0, 2.618, 3.0, 3.5, 4.0]
results_original = check_equation(R_test, r_test, phi_test_original)
save_results_to_csv(results_original, 'acceleration_results_original.csv')

print("\nWyniki:")
for phi, acceleration in results_original:
    print(f"φ = {phi:.4f}, a = {acceleration:.6f}")

# Test 2: Dense sampling around the critical point
print("\n" + "=" * 60)
print("TEST 2: Zagęszczona próbka wokół punktu krytycznego (2.618)")
print("=" * 60)
phi_test_dense = [1.0, 1.5, 2.0, 2.5, 2.6, 2.618, 2.62, 2.65, 2.7, 3.0, 3.5, 4.0]
results_dense = check_equation(R_test, r_test, phi_test_dense)
save_results_to_csv(results_dense, 'acceleration_results_dense.csv')

print("\nWyniki (szczególna uwaga na zakres 2.5 - 2.7):")
for phi, acceleration in results_dense:
    marker = " <-- STREFA KRYTYCZNA" if 2.5 <= phi <= 2.7 else ""
    print(f"φ = {phi:.4f}, a = {acceleration:.6f}{marker}")

# Test 3: Ultra-dense sampling for inflection point analysis
print("\n" + "=" * 60)
print("TEST 3: Ultra-zagęszczona próbka (co 0.05 w okolicach 2.618)")
print("=" * 60)
phi_test_ultra = (
    [i * 0.1 for i in range(10, 26)] +  # 1.0 do 2.5
    [2.5 + i * 0.01 for i in range(0, 21)] +  # 2.5 do 2.7 (co 0.01)
    [2.7 + i * 0.1 for i in range(1, 4)]  # 2.8 do 4.0
)
phi_test_ultra = sorted(set(phi_test_ultra))  # Remove duplicates and sort
results_ultra = check_equation(R_test, r_test, phi_test_ultra)
save_results_to_csv(results_ultra, 'acceleration_results_ultra.csv')

print(f"\nLiczba próbek: {len(results_ultra)}")
print("Wyniki (strefa krytyczna 2.5 - 2.7):")
for phi, acceleration in results_ultra:
    if 2.5 <= phi <= 2.7:
        derivative_estimate = None
        marker = " <-- STREFA KRYTYCZNA"
        print(f"φ = {phi:.4f}, a = {acceleration:.6f}{marker}")

# Visualization
print("\n" + "=" * 60)
print("GENEROWANIE WYKRESÓW")
print("=" * 60)
plot_results(results_original, title="Acceleration vs Phi (Original Sampling)", filename='acceleration_plot_original.png')
plot_results(results_dense, title="Acceleration vs Phi (Dense Sampling - Critical Region)", filename='acceleration_plot_dense.png')
plot_results(results_ultra, title="Acceleration vs Phi (Ultra-Dense Sampling)", filename='acceleration_plot_ultra.png')

# Analysis
print("\n" + "=" * 60)
print("ANALIZA PUNKTU KRYTYCZNEGO")
print("=" * 60)

# Find min and max in critical region
critical_region = [(phi, a) for phi, a in results_ultra if 2.5 <= phi <= 2.7]
if critical_region:
    min_phi, min_a = min(critical_region, key=lambda x: x[1])
    max_phi, max_a = max(critical_region, key=lambda x: x[1])
    
    print(f"\nW strefie 2.5 - 2.7:")
    print(f"  Minimum: φ = {min_phi:.4f}, a = {min_a:.6f}")
    print(f"  Maksimum: φ = {max_phi:.4f}, a = {max_a:.6f}")
    print(f"  Skok przyspieszenia: Δa = {max_a - min_a:.6f}")
    print(f"  Relatywna zmiana: {((max_a - min_a) / min_a * 100) if min_a != 0 else 'N/A'}%")
    
    # Check if it's a sharp cliff or smooth curve
    diffs = []
    for i in range(1, len(critical_region)):
        phi_diff = critical_region[i][0] - critical_region[i-1][0]
        a_diff = critical_region[i][1] - critical_region[i-1][1]
        if phi_diff != 0:
            diffs.append(a_diff / phi_diff)
    
    if diffs:
        print(f"\n  Średnia pochodna w strefie krytycznej: {sum(diffs) / len(diffs):.6f}")
        print(f"  Maksymalna pochodna: {max(diffs):.6f}")
        print(f"  Charakter: {'OSTRY (jak klif)' if max(diffs) > 10 else 'PŁYNNY (łagodne wzniesienie)'}")

print("\n" + "=" * 60)
print("WNIOSKI")
print("=" * 60)
print("• Wizualizacja pokazuje zachowanie przyspieszenia względem φ")
print("• Punkt krytyczny przy φ ≈ 2.618 to punkt przegięcia lub załamania krzywej")
print("• Zagęszczone próbki ujawniają, czy przejście jest ostre czy płynne")
print("• To określa precyzję wymaganą w rzeczywistej geometrii systemu")
