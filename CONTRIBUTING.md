# Contributing to Toroidal Flow Stabilization via the Golden Ratio

Thank you for your interest in contributing to this open-source research project. This document outlines how you can help advance our understanding of toroidal dynamics and the golden ratio's role in flow stabilization.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
3. [Reporting Issues](#reporting-issues)
4. [Submitting Results](#submitting-results)
5. [Development Workflow](#development-workflow)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation Standards](#documentation-standards)
8. [Pull Request Process](#pull-request-process)

---

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- **Be respectful** of diverse perspectives and backgrounds
- **Give constructive feedback** with the goal of improving the work
- **Acknowledge contributions** and credit collaborators
- **Report misconduct** to the project maintainers

---

## How to Contribute

### 1. **Theoretical Insights & Modeling**

If you have ideas to improve the governing equation or expand the theoretical framework:

- Open a **Discussion** or **Issue** with the tag `[Theory]`
- Propose alternative formulations or refinements to the centripetal acceleration model
- Suggest connections to other golden ratio phenomena in physics
- Share mathematical proofs or dimensional analysis

### 2. **Computational & Numerical Work**

Contributions to simulation accuracy and efficiency:

- **Parameter studies**: Test different values of R, r, and ω; explore sensitivity
- **Refinements**: Implement higher-order numerical schemes (e.g., spline interpolation)
- **Optimization**: Add multi-threading or GPU acceleration using CuPy
- **New integrators**: Propose Runge-Kutta or adaptive step methods for finer detail

### 3. **Experimental Validation**

Real-world data strengthens the research:

- **Physical experiments**: Conduct measurements in toroidal flows (cyclones, vortex reactors, etc.)
- **CFD verification**: Run simulations in ANSYS Fluent, OpenFOAM, COMSOL, or similar
- **Data submission**: Add your results to a dedicated `experiments/` directory with metadata

### 4. **Visualization & Analysis**

Help make results more accessible:

- **Interactive plots**: Create Plotly/Bokeh dashboards for parameter exploration
- **3D rendering**: Develop 3D toroidal flow visualizations
- **Statistical summaries**: Compute confidence intervals, sensitivity indices
- **Animation**: Create videos showing flow evolution over parameter ranges

### 5. **Documentation & Outreach**

Improve clarity and accessibility:

- **Translations**: Translate documentation to other languages
- **Educational materials**: Write tutorials for students and practitioners
- **Blog posts**: Share insights on toroidal systems or the golden ratio
- **Slides & presentations**: Create figures suitable for conferences

### 6. **Software Engineering**

Enhance code quality and maintainability:

- **Unit tests**: Add pytest coverage for edge cases
- **Performance profiling**: Benchmark and optimize hot paths
- **Refactoring**: Improve code clarity and structure
- **CI/CD**: Set up automated testing via GitHub Actions

---

## Reporting Issues

### Bug Reports

If you find an error or unexpected behavior:

1. **Check existing issues** — avoid duplicates
2. **Create a new issue** with the label `[Bug]`
3. **Include**:
   - Python version and OS
   - Steps to reproduce
   - Expected vs. actual output
   - Stack trace or error message
   - Sample data if applicable

**Example**:
```
Title: [Bug] Ultra-dense sampling crashes with large arrays

Description:
When running Test 3 with phi_test_ultra containing >1000 points, the code raises:
  MemoryError: Unable to allocate X GB

Steps:
1. Modify acceleration_simulation.py to use finer step size
2. Run `python acceleration_simulation.py`

Environment:
- Python 3.10.11
- RAM: 8 GB
- matplotlib 3.8.4
```

### Feature Requests

Have an idea for improvement?

1. **Create an issue** with the label `[Feature Request]`
2. **Describe**:
   - What problem it solves
   - Why it's valuable for the project
   - Rough implementation idea (optional)

---

## Submitting Results

### Adding Experimental or Computational Data

1. **Create a directory** under `experiments/` or `results/` named after your contribution:
   ```
   experiments/
   └── cyclone_validation_2026/
       ├── metadata.json
       ├── data.csv
       ├── plots/
       └── README.md
   ```

2. **Include metadata** (`metadata.json`):
   ```json
   {
     "title": "Cyclone Separator Validation",
     "author": "Your Name",
     "date": "2026-07-15",
     "institution": "Your University/Company",
     "method": "Experimental/CFD/Analytical",
     "tool": "Physical measurement / ANSYS Fluent / etc.",
     "parameters": {
       "R": 10.0,
       "r": 1.0,
       "omega": 2.5,
       "viscosity": "0.001 Pa·s"
     },
     "results": "Confirmed inflection point at φ ≈ 2.618",
     "doi": "10.1234/example.doi"
   }
   ```

3. **Add a README** explaining:
   - Source and measurement/simulation methodology
   - Data format and units
   - Key findings and comparison to model predictions
   - Limitations and uncertainties

4. **Submit via Pull Request** (see [Pull Request Process](#pull-request-process))

---

## Development Workflow

### 1. Fork & Clone

```bash
git clone https://github.com/<your-username>/fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio..git
cd fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio.
```

### 2. Create a Feature Branch

Use descriptive names:

```bash
git checkout -b feature/inflection-point-refinement
# or
git checkout -b fix/csv-export-bug
# or
git checkout -b experiment/3d-turbulence-model
```

### 3. Install Development Dependencies

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8
```

### 4. Make Changes

- Write clear, commented code
- Follow [PEP 8](https://pep8.org/) style guidelines
- Format with `black`:
  ```bash
  black acceleration_simulation.py
  ```
- Lint with `flake8`:
  ```bash
  flake8 acceleration_simulation.py
  ```

### 5. Commit with Clear Messages

```bash
git add .
git commit -m "feat: add 3D turbulence model for toroidal flows

- Implement RANS k-epsilon solver
- Add mesh refinement near φ = 2.618
- Validate against experimental data from cyclone rig
- Closes #42"
```

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code restructuring

---

## Testing Guidelines

### Running Tests

```bash
pytest tests/ -v --cov=acceleration_simulation
```

### Writing Tests

Create `tests/test_acceleration.py`:

```python
import pytest
from acceleration_simulation import check_equation

def test_zero_acceleration_at_unity_phi():
    """At φ=1.0, acceleration should be zero (formula special case)."""
    results = check_equation(R=10, r=1, phi_list=[1.0])
    assert results[0][1] == 0.0

def test_inflection_at_golden_ratio_squared():
    """Verify acceleration discontinuity near φ² ≈ 2.618."""
    results = check_equation(R=10, r=1, phi_list=[2.618])
    a_critical = results[0][1]
    assert a_critical > 10.0  # Dramatic jump

def test_monotonic_growth_before_critical():
    """Acceleration should grow monotonically for φ < 2.5."""
    phi_list = [1.0, 1.5, 2.0, 2.4]
    results = check_equation(R=10, r=1, phi_list=phi_list)
    accelerations = [r[1] for r in results]
    
    for i in range(len(accelerations) - 1):
        assert accelerations[i] < accelerations[i+1]
```

---

## Documentation Standards

### Code Comments

```python
def check_equation(R, r, phi_list, omega=1.0):
    """
    Compute centripetal acceleration in toroidal flow.
    
    Parameters:
    -----------
    R : float
        Major radius or reference distance (m)
    r : float
        Minor radius or secondary offset (m)
    phi_list : list of float
        Angular parameters (dimensionless)
    omega : float, optional
        Angular velocity in rad/s (default: 1.0)
    
    Returns:
    --------
    results : list of tuple
        Each tuple is (phi, acceleration_value)
    
    Notes:
    ------
    The golden ratio inflection point occurs at phi ≈ √2.618.
    For stability analysis, pay attention to regions 2.5 ≤ φ ≤ 2.7.
    """
```

### File Headers

```python
"""
Module: acceleration_simulation.py
Purpose: Simulate centripetal acceleration in toroidal systems
Author: Maciej Ziara
Date: 2026-07-13
License: MIT

Description:
    This module implements the three-stage sampling strategy for detecting
    critical bifurcation points in toroidal flow systems near the golden ratio.
"""
```

---

## Pull Request Process

### 1. Before Submitting

- [ ] Run tests: `pytest tests/ -v`
- [ ] Check linting: `flake8 .`
- [ ] Format code: `black .`
- [ ] Update README if needed
- [ ] Update CHANGELOG.md
- [ ] Verify all CSV/JSON exports work
- [ ] Check that plots generate without errors

### 2. Create PR on GitHub

**Title**: Concise, follows conventional commit style  
**Description**: Use the template below

```markdown
## Description
Brief summary of changes and motivation.

## Fixes
Closes #123

## Type of Change
- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Experimental validation
- [ ] Documentation
- [ ] Theory/Mathematical refinement

## Testing
Describe tests added or how changes were validated.

## Screenshots/Plots (if applicable)
Attach before/after comparisons or new visualizations.

## Checklist
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation updated
- [ ] No merge conflicts
```

### 3. Review & Feedback

- Respond promptly to review comments
- Update your branch based on feedback: `git push --force-with-lease`
- Request re-review once changes are made

### 4. Merge

Once approved, your PR will be merged by a project maintainer.

---

## Questions?

- **GitHub Discussions**: Ask general questions in the project Discussions tab
- **Issues**: Report specific problems with the label `[Question]`
- **Email**: Contact maciej.ziara@gmail.com for major collaboration proposals

---

## Recognition

We acknowledge all contributions in:
- `CONTRIBUTORS.md` (cumulative list)
- Release notes (per version)
- Project website (when established)

Thank you for helping advance open-source research in toroidal dynamics! 🚀

---

**Last Updated**: 2026-07-13  
**Maintained by**: Maciej Ziara
