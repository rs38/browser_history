# Browser History Analysis

This repository contains a Jupyter notebook and supporting scripts for analyzing and visualizing browser history data exported from a browser. The goal is to provide quick insights into visited domains, search queries, and trends over time.

The notebooks are published as a **JupyterLite site** — a fully self-contained web application that runs entirely in your browser with no backend server required.

## Table of Contents

- [Contents](#contents)
- [Quick Start — Run Locally](#quick-start--run-locally)
- [Usage (Classic Jupyter)](#usage-classic-jupyter)
- [Dependency Management](#dependency-management)
- [Deploying to GitHub Pages](#deploying-to-github-pages)
- [Development Notes](#development-notes)
- [Project Structure](#project-structure)
- [License](#license)

## Contents

- `browser_history_domain_overview.ipynb` – Main analysis notebook that loads CSV data, extracts domains, categorizes Google search queries, and plots activity.
- `browser_history_topic_overview.ipynb` – Topic analysis and classification notebook.
- `initialisation.py` – Helper functions for domain extraction and data loading.
- `dist/` – Pre-built JupyterLite site (HTML, JavaScript, assets); ready to serve or deploy to GitHub Pages.
- `jupyter_lite_config.json` – Configuration for building the JupyterLite site.
- `pyproject.toml` – Python project configuration with dependencies.

## Quick Start — Run Locally

### Prerequisites
- Python 3.10+ with `pip`
- `jupyterlite-core` and `jupyterlite-pyodide-kernel` (install below)

### Build & Serve

1. **Install JupyterLite tools:**
   ```bash
   pip install jupyterlite-core jupyterlite-pyodide-kernel
   ```

2. **Build the site:**
   ```bash
   rm -rf dist
   jupyter lite build --output-dir dist
   ```

3. **Start a local web server:**
   ```bash
   python3 -m http.server 8000 --directory dist
   ```

4. **Open in your browser:**
   ```
   http://localhost:8000/lab
   ```

5. **Access your notebooks:**
   - Navigate via the **File Browser** (left sidebar) → `files/` folder
   - Or open directly:
     - `http://localhost:8000/lab?path=files/browser_history_domain_overview.ipynb`
     - `http://localhost:8000/lab?path=files/browser_history_topic_overview.ipynb`

### Upload Your Browser History CSV

1. In JupyterLite, use the **File Browser** → upload your exported CSV (drag-and-drop or right-click → Upload)
2. Update the notebook cell with the correct CSV filename
3. Run all cells to generate analysis and visualizations

## Usage (Classic Jupyter)

For local development with standard Jupyter:

1. Export your browser history to a CSV file
2. Place the CSV in the repository root
3. Open `browser_history_domain_overview.ipynb` in Jupyter/VS Code
4. Run cells sequentially to reproduce the analysis

## Dependency Management

### Local Development

Python dependencies are listed in `pyproject.toml`. Install with:

```bash
uv install
```

The notebooks use:
- `pandas` for CSV handling and aggregation
- `matplotlib` for plotting
- `scikit-learn` for topic classification (optional)

### In JupyterLite (Browser)

The JupyterLite environment has `pandas`, `numpy`, and `matplotlib` pre-installed via Pyodide. Additional packages can be installed inside notebook cells using:

```python
%pip install <package-name>
```

Note: Not all packages are available in Pyodide. Complex C extensions may not work.

## Deploying to GitHub Pages

The site is automatically deployed via GitHub Actions (`.github/workflows/deploy.yml`) when you push to `main`:

1. The workflow builds the JupyterLite site into the `dist/` folder
2. GitHub Actions uploads `dist/` as a GitHub Pages artifact
3. Your site is live at `https://<username>.github.io/<repo>/`

**To deploy manually:**
```bash
jupyter lite build --output-dir dist
# Then push the dist/ folder to GitHub Pages or any static host
```

## Development Notes

- **Domain extraction** — Uses `urllib.parse` with normalization and `www.` stripping
- **Google search parsing** — Extracts queries from URLs; detects AI Overview (`udm=50` parameter)
- **Topic classification** — Keyword-based categorization; easily extensible
- **Refer to** [copilot-instructions.md](.github/copilot-instructions.md) for analysis patterns

## Project Structure

```
browser_history/
├── browser_history_domain_overview.ipynb   # Main analysis notebook
├── browser_history_topic_overview.ipynb    # Topic analysis notebook
├── initialisation.py                        # Helper functions
├── jupyter_lite_config.json                 # JupyterLite config
├── dist/                                    # Pre-built JupyterLite site
│   ├── index.html
│   ├── lab/
│   ├── api/
│   ├── extensions/
│   ├── files/                               # Uploaded CSV & notebooks
│   └── ...                                  # Static assets
├── .github/workflows/deploy.yml             # CI/CD for GitHub Pages
├── pyproject.toml                           # Python dependencies
└── README.md                                # This file
```

## License

Add your preferred license here.
