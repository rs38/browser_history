# Browser History Analysis

This repository contains a Jupyter notebook and supporting scripts for analyzing and visualizing browser history data exported from a browser. The goal is to provide quick insights into visited domains, search queries, and trends over time.

## Contents

- `browser_history_domain_overview.ipynb` – Main analysis notebook that loads CSV data, extracts domains, categorizes Google search queries, and plots activity.
- `BrowserHistory_22.02.26.csv` – Example export of browser history used for development and testing.
- `main.py` – (if used) placeholder script for programmatic access or automation.
- `pyproject.toml` – Python project configuration with dependencies. Uses pandas and matplotlib.
- `README.md` – This file.

## Usage

1. Export your browser history to a CSV file (format shown in example).
2. Place the CSV in the repository root and update the `csv_path` variable in the notebook if needed.
3. Open `browser_history_domain_overview.ipynb` in Jupyter or VS Code and run the cells sequentially to reproduce the analysis.
4. Modify or extend the notebook with additional sections as desired (see comments for patterns).

## Dependency Management

Python dependencies are listed in `pyproject.toml`. Install them with:

```powershell
uv install
```

The notebook uses:

- `pandas` for CSV handling and aggregation
- `matplotlib` for plotting

When adding new libraries, update the project file accordingly.

## Development Notes

- Domain extraction is handled via `urllib.parse` with normalization and `www.` stripping.
- Google search query parsing uses `urlparse` and `parse_qs` with support for AI overview detection (`udm=50`).
- Topic classification can be customized by editing the `classify_search_topic` function in the notebook; keywords and categories can be expanded.
- Refer to [copilot-instructions.md](.github/copilot-instructions.md) for analysis patterns and conventions.

## License

Add your preferred license here.
