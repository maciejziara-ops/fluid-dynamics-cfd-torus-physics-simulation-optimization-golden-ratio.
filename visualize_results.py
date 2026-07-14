import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def generate_visualization():
    """Generuje wykresy porównawcze modelu idealnego i modelu z lepkością."""
    
    # Wczytanie danych
    df = pd.read_csv('acceleration_viscosity_comparison.csv')
    
    phi = df['phi'].values
    a_ideal = df['acceleration_ideal'].values
    a_viscous = df['acceleration_viscous'].values
    grad_ideal = df['gradient_ideal'].values
    grad_viscous = df['gradient_viscous'].values
    
    # Tworzenie figury z 4 subplotami
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Analiza Modelu Lepkości Turbulentnej w Geometrii Torusa', fontsize=16, fontweight='bold')
    
    # Plot 1: Porównanie przyspieszenia
    ax1 = axes[0, 0]
    ax1.plot(phi, a_ideal, label='Model Idealny (bez lepkości)', linewidth=2, color='red', alpha=0.7)
    ax1.plot(phi, a_viscous, label='Model z Lepkością', linewidth=2, color='blue', alpha=0.7)
    ax1.axvline(x=np.sqrt(2.6180339887), color='green', linestyle='--', linewidth=1.5, label='Punkt Krytyczny (φ² ≈ 2.618)')
    ax1.set_xlabel('φ', fontsize=11)
    ax1.set_ylabel('Przyspieszenie Dośrodkowe (a)', fontsize=11)
    ax1.set_title('Profil Przyspieszenia', fontsize=12, fontweight='bold')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Tłumienie (Damping Factor)
    ax2 = axes[0, 1]
    damping_factor = 1.0 - 0.65 * np.exp(-((phi - np.sqrt(2.6180339887)) / 0.35)**2)
    ax2.plot(phi, damping_factor, linewidth=2.5, color='purple')
    ax2.axvline(x=np.sqrt(2.6180339887), color='green', linestyle='--', linewidth=1.5, label='Punkt Krytyczny')
    ax2.fill_between(phi, 0, damping_factor, alpha=0.3, color='purple')
    ax2.set_xlabel('φ', fontsize=11)
    ax2.set_ylabel('Współczynnik Tłumienia', fontsize=11)
    ax2.set_title('Dynamiczny Czynnik Lepkości (Gaussian Damping)', fontsize=12, fontweight='bold')
    ax2.set_ylim([0, 1.05])
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Porównanie gradientów
    ax3 = axes[1, 0]
    ax3.plot(phi, grad_ideal, label='Gradient - Model Idealny', linewidth=2, color='red', alpha=0.7)
    ax3.plot(phi, grad_viscous, label='Gradient - Model z Lepkością', linewidth=2, color='blue', alpha=0.7)
    ax3.axvline(x=np.sqrt(2.6180339887), color='green', linestyle='--', linewidth=1.5, label='Punkt Krytyczny')
    ax3.set_xlabel('φ', fontsize=11)
    ax3.set_ylabel('Pochodna (da/dφ)', fontsize=11)
    ax3.set_title('Analiza Stabilności - Gradienty', fontsize=12, fontweight='bold')
    ax3.legend(loc='best')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Zmiana względna (procentowa)
    ax4 = axes[1, 1]
    change_percent = np.where(a_ideal != 0, (a_ideal - a_viscous) / a_ideal * 100, 0)
    ax4.plot(phi, change_percent, linewidth=2.5, color='orange')
    ax4.axvline(x=np.sqrt(2.6180339887), color='green', linestyle='--', linewidth=1.5, label='Punkt Krytyczny')
    ax4.axhline(y=65, color='red', linestyle=':', linewidth=1.5, label='Zakładane tłumienie (65%)')
    ax4.fill_between(phi, 0, change_percent, alpha=0.3, color='orange')
    ax4.set_xlabel('φ', fontsize=11)
    ax4.set_ylabel('Zmiana Względna (%)', fontsize=11)
    ax4.set_title('Redukcja Przyspieszenia (%)', fontsize=12, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('viscosity_analysis_report.png', dpi=300, bbox_inches='tight')
    print("✅ Wykres zapisany: viscosity_analysis_report.png")
    
    # Tworzenie wykresu zbliżenia (zoom na punkt krytyczny)
    fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))
    fig2.suptitle('Szczegółowa Analiza w Pobliżu Punktu Krytycznego (φ² ≈ 2.618)', fontsize=14, fontweight='bold')
    
    phi_crit = np.sqrt(2.6180339887)
    zoom_mask = (phi >= phi_crit - 0.5) & (phi <= phi_crit + 0.5)
    phi_zoom = phi[zoom_mask]
    a_ideal_zoom = a_ideal[zoom_mask]
    a_viscous_zoom = a_viscous[zoom_mask]
    
    ax5 = axes2[0]
    ax5.plot(phi_zoom, a_ideal_zoom, label='Model Idealny', linewidth=2.5, color='red', marker='o', markersize=3, alpha=0.7)
    ax5.plot(phi_zoom, a_viscous_zoom, label='Model z Lepkością', linewidth=2.5, color='blue', marker='s', markersize=3, alpha=0.7)
    ax5.axvline(x=phi_crit, color='green', linestyle='--', linewidth=2, label='Punkt Krytyczny')
    ax5.set_xlabel('φ', fontsize=11)
    ax5.set_ylabel('Przyspieszenie', fontsize=11)
    ax5.set_title('Zoom: Przyspieszenie', fontsize=12, fontweight='bold')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    grad_ideal_zoom = grad_ideal[zoom_mask]
    grad_viscous_zoom = grad_viscous[zoom_mask]
    
    ax6 = axes2[1]
    ax6.plot(phi_zoom, grad_ideal_zoom, label='Gradient - Model Idealny', linewidth=2.5, color='red', marker='o', markersize=3, alpha=0.7)
    ax6.plot(phi_zoom, grad_viscous_zoom, label='Gradient - Model z Lepkością', linewidth=2.5, color='blue', marker='s', markersize=3, alpha=0.7)
    ax6.axvline(x=phi_crit, color='green', linestyle='--', linewidth=2, label='Punkt Krytyczny')
    ax6.set_xlabel('φ', fontsize=11)
    ax6.set_ylabel('Gradient (da/dφ)', fontsize=11)
    ax6.set_title('Zoom: Gradient Stabilności', fontsize=12, fontweight='bold')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('viscosity_critical_point_zoom.png', dpi=300, bbox_inches='tight')
    print("✅ Wykres zoom zapisany: viscosity_critical_point_zoom.png")
    
    plt.close('all')

if __name__ == "__main__":
    generate_visualization()
