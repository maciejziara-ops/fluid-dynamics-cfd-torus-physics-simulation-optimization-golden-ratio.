"""
Test suite for acceleration_simulation.py

This module contains comprehensive unit tests for the toroidal flow
acceleration simulation using pytest.

Run tests with:
    pytest tests/test_acceleration.py -v --cov=acceleration_simulation
"""

import pytest
import os
import json
import csv
from pathlib import Path
import tempfile
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from acceleration_simulation import check_equation, save_results_to_csv, save_results_to_json, save_results_to_txt


class TestCheckEquation:
    """Test the core acceleration computation function."""
    
    def test_zero_acceleration_at_phi_one(self):
        """At φ=1.0, acceleration should be zero (special case in formula)."""
        results = check_equation(R=10, r=1, phi_list=[1.0])
        assert len(results) == 1
        assert results[0][0] == 1.0
        assert abs(results[0][1] - 0.0) < 1e-10  # Near-zero within floating point precision
    
    def test_returns_list_of_tuples(self):
        """check_equation should return list of (phi, acceleration) tuples."""
        results = check_equation(R=10, r=1, phi_list=[1.0, 2.0, 3.0])
        assert isinstance(results, list)
        assert len(results) == 3
        for item in results:
            assert isinstance(item, tuple)
            assert len(item) == 2
    
    def test_positive_acceleration(self):
        """Acceleration values should be non-negative."""
        results = check_equation(R=10, r=1, phi_list=[1.5, 2.0, 2.5, 3.0])
        for phi, acceleration in results:
            assert acceleration >= 0, f"Negative acceleration at φ={phi}"
    
    def test_acceleration_growth_before_critical(self):
        """Acceleration should generally increase for φ < 2.5."""
        phi_list = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4]
        results = check_equation(R=10, r=1, phi_list=phi_list)
        accelerations = [r[1] for r in results]
        
        # Check monotonic growth (with tolerance for floating point)
        for i in range(len(accelerations) - 1):
            assert accelerations[i] <= accelerations[i+1] + 1e-10, \
                f"Non-monotonic at indices {i}, {i+1}: {accelerations[i]} > {accelerations[i+1]}"
    
    def test_critical_point_at_golden_ratio_squared(self):
        """Verify acceleration is significantly higher at φ ≈ 2.618."""
        results_before = check_equation(R=10, r=1, phi_list=[2.5])
        results_critical = check_equation(R=10, r=1, phi_list=[2.618])
        results_after = check_equation(R=10, r=1, phi_list=[2.7])
        
        a_before = results_before[0][1]
        a_critical = results_critical[0][1]
        a_after = results_after[0][1]
        
        # Critical point should have much higher acceleration
        assert a_critical > 10 * a_before, \
            f"Expected a_critical >> a_before, got {a_critical} vs {a_before}"
    
    def test_inflection_point_sharpness(self):
        """Test that the inflection at φ ≈ 2.618 is sharp (cliff-like)."""
        # Dense sampling around critical point
        phi_list = [2.61, 2.615, 2.618, 2.620, 2.625]
        results = check_equation(R=10, r=1, phi_list=phi_list)
        accelerations = [r[1] for r in results]
        
        # Find max and min
        max_accel = max(accelerations)
        min_accel = min(accelerations)
        
        # Relative jump should be significant
        relative_jump = (max_accel - min_accel) / (min_accel + 1e-10)
        assert relative_jump > 100, f"Inflection not sharp enough: {relative_jump}x increase"
    
    def test_different_R_values(self):
        """Acceleration should vary with major radius R."""
        results_R10 = check_equation(R=10, r=1, phi_list=[2.0])
        results_R20 = check_equation(R=20, r=1, phi_list=[2.0])
        
        a_R10 = results_R10[0][1]
        a_R20 = results_R20[0][1]
        
        # Different R should produce different accelerations
        assert a_R10 != a_R20, "R parameter has no effect on acceleration"
    
    def test_different_r_values(self):
        """Acceleration should vary with minor radius r."""
        results_r1 = check_equation(R=10, r=1, phi_list=[2.0])
        results_r2 = check_equation(R=10, r=2, phi_list=[2.0])
        
        a_r1 = results_r1[0][1]
        a_r2 = results_r2[0][1]
        
        # Different r should produce different accelerations
        assert a_r1 != a_r2, "r parameter has no effect on acceleration"
    
    def test_omega_squared_scaling(self):
        """Acceleration should scale as ω²."""
        results_omega1 = check_equation(R=10, r=1, phi_list=[2.0], omega=1.0)
        results_omega2 = check_equation(R=10, r=1, phi_list=[2.0], omega=2.0)
        
        a_omega1 = results_omega1[0][1]
        a_omega2 = results_omega2[0][1]
        
        # Should scale as omega^2
        expected_ratio = 4.0  # (2.0/1.0)^2
        actual_ratio = a_omega2 / (a_omega1 + 1e-10)
        
        assert abs(actual_ratio - expected_ratio) < 0.01, \
            f"Expected {expected_ratio}x scaling, got {actual_ratio}x"
    
    def test_empty_phi_list(self):
        """Should handle empty phi_list gracefully."""
        results = check_equation(R=10, r=1, phi_list=[])
        assert results == []
    
    def test_single_phi_value(self):
        """Should handle single phi value."""
        results = check_equation(R=10, r=1, phi_list=[2.618])
        assert len(results) == 1
    
    def test_large_phi_values(self):
        """Should handle large phi values without errors."""
        results = check_equation(R=10, r=1, phi_list=[10.0, 100.0, 1000.0])
        assert len(results) == 3
        assert all(a >= 0 for _, a in results)


class TestSaveResultsToCSV:
    """Test CSV export functionality."""
    
    def test_csv_file_created(self):
        """CSV file should be created successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = [(1.0, 0.0), (2.0, 0.3), (3.0, 1.8)]
            filepath = os.path.join(tmpdir, 'test_results.csv')
            
            save_results_to_csv(results, filename=filepath)
            
            assert os.path.exists(filepath), "CSV file not created"
    
    def test_csv_format_correctness(self):
        """CSV should have correct headers and data format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = [(1.0, 0.0), (2.0, 0.3), (3.0, 1.8)]
            filepath = os.path.join(tmpdir, 'test_results.csv')
            
            save_results_to_csv(results, filename=filepath)
            
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
            
            # Check header
            assert rows[0] == ['phi', 'acceleration'], "CSV header incorrect"
            
            # Check data rows
            assert len(rows) == 4, f"Expected 4 rows (header + 3 data), got {len(rows)}"
            assert rows[1] == ['1.0', '0.0']
            assert rows[2] == ['2.0', '0.3']
            assert rows[3] == ['3.0', '1.8']
    
    def test_csv_roundtrip(self):
        """Data should be recoverable from CSV."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_results = [(1.0, 0.0), (2.0, 0.3), (3.0, 1.8)]
            filepath = os.path.join(tmpdir, 'test_results.csv')
            
            save_results_to_csv(original_results, filename=filepath)
            
            # Read back
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                recovered_results = [(float(row['phi']), float(row['acceleration'])) for row in reader]
            
            assert recovered_results == original_results


class TestSaveResultsToJSON:
    """Test JSON export functionality."""
    
    def test_json_file_created(self):
        """JSON file should be created successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = [(1.0, 0.0), (2.0, 0.3), (3.0, 1.8)]
            filepath = os.path.join(tmpdir, 'test_results.json')
            
            save_results_to_json(results, filename=filepath)
            
            assert os.path.exists(filepath), "JSON file not created"
    
    def test_json_structure(self):
        """JSON should have correct metadata and data structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = [(1.0, 0.0), (2.0, 0.3)]
            filepath = os.path.join(tmpdir, 'test_results.json')
            
            save_results_to_json(results, filename=filepath)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Check structure
            assert 'metadata' in data, "Missing 'metadata' key"
            assert 'data' in data, "Missing 'data' key"
            
            # Check metadata
            metadata = data['metadata']
            assert metadata['R'] == 10
            assert metadata['r'] == 1
            assert metadata['omega'] == 1.0
            assert metadata['total_samples'] == 2
            
            # Check data
            assert len(data['data']) == 2
            assert data['data'][0]['phi'] == 1.0
            assert data['data'][0]['acceleration'] == 0.0
    
    def test_json_roundtrip(self):
        """Data should be recoverable from JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_results = [(1.0, 0.0), (2.0, 0.3), (3.0, 1.8)]
            filepath = os.path.join(tmpdir, 'test_results.json')
            
            save_results_to_json(original_results, filename=filepath)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            recovered_results = [(item['phi'], item['acceleration']) for item in data['data']]
            assert recovered_results == original_results


class TestSaveResultsToTXT:
    """Test TXT export functionality."""
    
    def test_txt_file_created(self):
        """TXT file should be created successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = [(1.0, 0.0), (2.0, 0.3), (3.0, 1.8)]
            filepath = os.path.join(tmpdir, 'test_results.txt')
            
            save_results_to_txt(results, filename=filepath)
            
            assert os.path.exists(filepath), "TXT file not created"
    
    def test_txt_contains_parameters(self):
        """TXT should contain simulation parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = [(1.0, 0.0), (2.0, 0.3)]
            filepath = os.path.join(tmpdir, 'test_results.txt')
            
            save_results_to_txt(results, filename=filepath)
            
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Check for key information
            assert 'R' in content and '10' in content
            assert 'r' in content and '1' in content
            assert 'ω' in content
            assert 'Równanie' in content or 'equation' in content.lower()
    
    def test_txt_contains_data(self):
        """TXT should contain the data values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = [(1.0, 0.0), (2.0, 0.3)]
            filepath = os.path.join(tmpdir, 'test_results.txt')
            
            save_results_to_txt(results, filename=filepath)
            
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Check for data values
            assert '1.0000' in content or '1.0' in content
            assert '2.0000' in content or '2.0' in content
            assert '0.0' in content
            assert '0.3' in content
    
    def test_txt_contains_statistics(self):
        """TXT should contain statistical analysis."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = [(1.0, 0.5), (2.0, 1.5), (3.0, 3.0)]
            filepath = os.path.join(tmpdir, 'test_results.txt')
            
            save_results_to_txt(results, filename=filepath)
            
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Check for statistics
            assert 'Min' in content or 'minimum' in content.lower()
            assert 'Max' in content or 'maximum' in content.lower()


class TestIntegration:
    """Integration tests for full workflow."""
    
    def test_full_simulation_workflow(self):
        """Test complete simulation and export workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            
            # Run simulation
            phi_list = [1.0, 1.5, 2.0, 2.618, 3.0]
            results = check_equation(R=10, r=1, phi_list=phi_list)
            
            # Export to all formats
            save_results_to_csv(results, 'results.csv')
            save_results_to_json(results, 'results.json')
            save_results_to_txt(results, 'results.txt')
            
            # Verify all files exist
            assert os.path.exists('results.csv')
            assert os.path.exists('results.json')
            assert os.path.exists('results.txt')
            
            # Verify they contain same number of records
            with open('results.csv') as f:
                csv_rows = len(f.readlines()) - 1  # Exclude header
            
            with open('results.json') as f:
                json_data = json.load(f)
                json_rows = len(json_data['data'])
            
            assert csv_rows == json_rows == len(results)
    
    def test_ultra_dense_sampling(self):
        """Test ultra-dense sampling around critical point."""
        phi_test_ultra = (
            [i * 0.1 for i in range(10, 26)] +  # 1.0 do 2.5
            [2.5 + i * 0.01 for i in range(0, 21)] +  # 2.5 do 2.7
            [2.7 + i * 0.1 for i in range(1, 4)]  # 2.8 do 4.0
        )
        phi_test_ultra = sorted(set(phi_test_ultra))
        
        results = check_equation(R=10, r=1, phi_list=phi_test_ultra)
        
        # Should have significant number of points
        assert len(results) > 30, "Ultra-dense sampling should produce 30+ points"
        
        # Should detect critical region
        critical_region = [(phi, a) for phi, a in results if 2.5 <= phi <= 2.7]
        assert len(critical_region) > 10, "Critical region should have multiple points"
        
        # Critical region should show acceleration jump
        min_a = min(a for _, a in critical_region)
        max_a = max(a for _, a in critical_region)
        assert max_a > 10 * min_a, "Should show dramatic acceleration jump"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_negative_R_raises_error_or_gives_positive_result(self):
        """Function should handle negative R gracefully."""
        # The current implementation uses abs(), so should still work
        results = check_equation(R=-10, r=1, phi_list=[2.0])
        assert len(results) == 1
        assert results[0][1] >= 0
    
    def test_zero_omega(self):
        """With omega=0, acceleration should be zero."""
        results = check_equation(R=10, r=1, phi_list=[2.0], omega=0.0)
        assert results[0][1] == 0.0
    
    def test_very_large_phi(self):
        """Should handle very large phi values."""
        results = check_equation(R=10, r=1, phi_list=[1000.0])
        assert len(results) == 1
        assert results[0][1] >= 0
    
    def test_very_small_phi(self):
        """Should handle very small positive phi values."""
        results = check_equation(R=10, r=1, phi_list=[0.01])
        assert len(results) == 1
        # Acceleration should be close to zero or small


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
