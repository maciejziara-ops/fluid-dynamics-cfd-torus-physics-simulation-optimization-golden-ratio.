import csv
import math

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

# Parametry
R_test = 10
r_test = 1
# Dodajemy 2.618 bezpośrednio do listy, żeby zobaczyć punkt krytyczny
phi_test = [1.0, 1.5, 2.0, 2.618, 3.0, 3.5, 4.0]

# Run simulation
results = check_equation(R_test, r_test, phi_test)

# Save to CSV
save_results_to_csv(results)

# Optional: Print results to console
print("\nCalculated accelerations:")
for phi, acceleration in results:
    print(f"φ = {phi:.4f}, a = {acceleration:.6f}")
