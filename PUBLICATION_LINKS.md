# Publication Links & Digital Object Identifiers

## 🔗 Direct Repository Links

### Main Repository
**Repository URL:**
```
https://github.com/maciejziara-ops/fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio.
```

**Direct Access Points:**
- Code: https://github.com/maciejziara-ops/fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio./tree/main
- Issues: https://github.com/maciejziara-ops/fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio./issues
- Discussions: https://github.com/maciejziara-ops/fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio./discussions

---

## 📦 Release & Version Management

### GitHub Releases
To create an official release, use:

```bash
git tag -a v1.0.0 -m "Initial release: Viscous model with CFD validation"
git push origin v1.0.0
```

**Suggested Release Name:** `v1.0.0 - Viscous Damping Model with 31 Unit Tests`

**Release URL Template:**
```
https://github.com/maciejziara-ops/fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio./releases/tag/v1.0.0
```

**Release Notes Template:**
```markdown
# v1.0.0 - Viscous Damping Model with Golden Ratio Optimization

## What's New
- ✅ Dynamic turbulent viscosity model (65% damping at critical point)
- ✅ 10,000 sample point dataset
- ✅ Comprehensive test suite (16 + 15 CFD tests)
- ✅ Visualization tools
- ✅ Full documentation

## Assets
- viscous_model.py - Core calculation engine
- acceleration_viscosity_comparison.csv - Complete dataset
- visualize_results.py - Visualization script
- tests/ - 31 unit tests

## Test Results
- Basic Model Tests: 16/16 ✅
- CFD-Specific Tests: 15/15 ✅
- Pass Rate: 100%

## Publications & Citations
See PUBLICATION_LINKS.md for DOI and citation information.
```

---

## 🎓 DOI & Zenodo Integration

### Zenodo Archive Submission
To create a persistent DOI, follow these steps:

1. **Visit Zenodo:** https://zenodo.org
2. **Login** with GitHub account
3. **Connect** your GitHub repository
4. **Publish** with the following metadata:

#### Suggested Citation Metadata:
```bibtex
@software{ziara2026viscous,
  author = {Ziara, Maciej},
  title = {Fluid Dynamics CFD Torus Physics Simulation with 
           Viscous Damping and Golden Ratio Optimization},
  year = {2026},
  month = {July},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.XXXXXXX},
  url = {https://zenodo.org/record/XXXXXXX},
  github = {https://github.com/maciejziara-ops/fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio.}
}
```

#### Zenodo Metadata Fields:
- **Title:** Fluid Dynamics CFD Torus Physics Simulation with Viscous Damping and Golden Ratio Optimization
- **Author:** Maciej Ziara (maciejziara-ops)
- **Description:** Python implementation of turbulent viscosity model for toroidal geometry with dynamic Gaussian damping factor. Includes 10,000 sample points, comprehensive CFD validation (15 tests), numerical stability verification (16 tests), and visualization tools.
- **Keywords:** CFD, turbulent viscosity, toroidal flow, golden ratio, Python, numerical simulation
- **License:** MIT
- **Upload Type:** Software
- **Communities:** Computational Fluid Dynamics, Physics Simulations

#### Expected DOI Format:
```
https://doi.org/10.5281/zenodo.XXXXXXX
```

---

## 📚 GitHub Pages Documentation

### Enable GitHub Pages
1. Go to repository Settings → Pages
2. Select branch: `main`
3. Select folder: `/docs` or `/(root)`

### Create Documentation Site
Create `docs/index.md`:

```markdown
# Viscous Damping Model for Toroidal Flow

## Quick Start
1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Run model: `python viscous_model.py`
4. Generate visualizations: `python visualize_results.py`
5. Run tests: `python -m pytest tests/`

## Documentation
- [Model Theory](./theory.md)
- [API Reference](./api.md)
- [Test Results](./test-results.md)
- [Publications](./publications.md)

## Citation
```

### GitHub Pages URL:
```
https://maciejziara-ops.github.io/fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio./
```

### Deploy Script (`.github/workflows/pages.yml`):
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build docs
        run: |
          pip install mkdocs
          mkdocs build
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

---

## 📋 Complete Publication Strategy

### Phase 1: GitHub Release (Immediate)
```
Release: v1.0.0
URL: https://github.com/maciejziara-ops/.../releases/tag/v1.0.0
Format: GitHub Release with tagged commit
```

### Phase 2: Zenodo Archive (1-2 weeks)
```
DOI: 10.5281/zenodo.XXXXXXX
URL: https://zenodo.org/record/XXXXXXX
Indexing: CrossRef, DataCite, OpenAIRE
```

### Phase 3: GitHub Pages (Ongoing)
```
Documentation: https://maciejziara-ops.github.io/.../
Autoupdates: On every push to main
Features: Full API docs, test results, theory
```

### Phase 4: Academic Publication (Future)
```
Consider submission to:
- Journal of Computational Physics
- Computers & Fluids
- International Journal of CFD
- arXiv (1908.XXXXX)
```

---

## 🔍 Citation Examples

### BibTeX
```bibtex
@software{ziara2026viscous,
  author = {Ziara, Maciej},
  title = {Viscous Damping Model for Toroidal Flow with 
           Golden Ratio Optimization},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/maciejziara-ops/fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio.},
  doi = {10.5281/zenodo.XXXXXXX}
}
```

### APA
Ziara, M. (2026). Viscous damping model for toroidal flow with golden ratio optimization [Software]. GitHub. https://doi.org/10.5281/zenodo.XXXXXXX

### MLA
Ziara, Maciej. "Viscous Damping Model for Toroidal Flow with Golden Ratio Optimization." GitHub, 2026, https://github.com/maciejziara-ops/fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio., https://doi.org/10.5281/zenodo.XXXXXXX.

### Chicago
Ziara, Maciej. "Viscous Damping Model for Toroidal Flow with Golden Ratio Optimization." Accessed [Date]. https://github.com/maciejziara-ops/fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio.. https://doi.org/10.5281/zenodo.XXXXXXX.

---

## 📊 Impact Metrics

### GitHub Metrics
- Repository URL: https://github.com/maciejziara-ops/fluid-dynamics-cfd-torus-physics-simulation-optimization-golden-ratio.
- Stars: Track engagement
- Forks: Track adoption
- Issues: Community feedback

### Zenodo Metrics
- Views: Track accessibility
- Downloads: Track usage
- Citations: Track impact
- Dashboard: https://zenodo.org/account/settings/applications

---

## 🎯 Recommended Next Steps

1. **Create GitHub Release**
   - Tag: v1.0.0
   - Add comprehensive release notes
   - Attach documentation PDFs

2. **Submit to Zenodo**
   - Follow Zenodo GitHub integration
   - Receive DOI automatically
   - Enable future versions

3. **Enable GitHub Pages**
   - Create docs folder
   - Set up auto-deployment
   - Add API documentation

4. **Register with Registries**
   - PyPI (if distributing as package)
   - Zenodo Communities
   - GitHub Awesome Lists

---

## 📮 Long-Term Archival

### Persistent URLs
| Service | URL | Type | Expiry |
|---------|-----|------|--------|
| GitHub | https://github.com/maciejziara-ops/... | Repository | N/A |
| Zenodo | https://zenodo.org/record/XXXXXXX | DOI | Permanent |
| GitHub Pages | https://maciejziara-ops.github.io/... | Website | N/A |
| DataCite | https://doi.org/10.5281/zenodo.XXXXXXX | Metadata | Permanent |

---

**Generated:** 2026-07-14  
**Version:** 1.0.0  
**Status:** Ready for Publication  
**Last Updated:** 2026-07-14
