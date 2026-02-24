# JupyterLite Deployment Plan

## Goal
Deploy the browser history analysis notebooks as a publicly accessible JupyterLite site on GitHub Pages, runnable entirely in the browser.

---

## CI / Build Pipeline

- [x] Add `jupyter-server` to GitHub Actions workflow (`deploy.yml`) — was missing, caused build failure
- [x] Use `python -m pip install` instead of bare `pip` to ensure correct interpreter in CI
- [x] Install `jupyterlite-pyodide-kernel` in CI workflow
- [ ] Push `ci-fixes` branch to remote and open PR → merge to `main`
- [ ] Verify GitHub Actions build passes end-to-end after merge

---

## JupyterLite Site — Kernel & Extensions

- [x] Install `jupyterlite-pyodide-kernel` locally
- [x] Fix `federated_extensions: []` — pyodide kernel JS extension not found because pip installs to `~/.local` (user site), not `sys.prefix`. Fixed via `jupyter_lite_config.json` `FederatedExtensionAddon.extra_labextensions_path`
- [x] Verify `@jupyterlite/pyodide-kernel-extension` appears in `dist/jupyter-lite.json`
- [x] Confirm Python kernel is selectable in browser after page load (user verified working)

---

## Notebook — Dependencies

- [x] Add `%pip install pandas matplotlib numpy` cell at top of notebook (micropip in JupyterLite, pip locally)
- [ ] Verify all imports in `browser_history_topic_overview.ipynb` also work (scikit-learn etc.)

---

## Notebook — Module Import Fix

- [x] Add `initialisation.py` to `LiteBuildApp.contents` in `jupyter_lite_config.json`
- [x] Inline `extract_domain` and `load_history_df` from `initialisation.py` directly into the notebook cell — avoids `ModuleNotFoundError` because Pyodide's `sys.path` doesn't include the notebook directory

---

## Notebook — CSV Upload

- [x] Add markdown cell with upload instructions (drag-and-drop to sidebar, or use widget)
- [x] Add `FileUpload` widget cell (ipywidgets) that sets `CSV_FILENAME` on upload; falls back gracefully when running locally
- [x] Load cell uses `CSV_FILENAME` variable instead of hardcoded filename
- [ ] Verify `ipywidgets` FileUpload widget actually works in Pyodide kernel (may need `%pip install ipywidgets` added to pip cell)
- [ ] Test full round-trip: upload CSV → run all cells → see charts

---

## Local Dev / Test Server

- [x] HTTP server running at `http://127.0.0.1:8000/lab`
- [x] Notebooks accessible via File Browser in left sidebar at `dist/files/`
- [ ] Document rebuild + server commands in README:
  ```bash
  rm -rf dist
  jupyter lite build --output-dir dist
  python3 -m http.server 8000 --directory dist
  ```
  Then visit `http://localhost:8000/lab`

---

## Open Issues

- **Push blocked** — `ci-fixes` branch has 6 commits ahead of `origin/main` but push is blocked by missing write credentials in this environment. Must be pushed manually.
- **Hardcoded user path** — `jupyter_lite_config.json` contains `/home/fb/.local/share/jupyter/labextensions`. This is fine for local dev and CI (where `setup-python` installs to `sys.prefix`), but won't work for other developers. Consider replacing with a venv or a build script that injects the path dynamically.
- **`browser_history_topic_overview.ipynb`** — not yet checked for the same import / dependency issues.
- **Notebooks in dist/files/** — Notebooks are placed in `files/` subdirectory rather than root. Access via File Browser or direct URL: `http://localhost:8000/lab?path=files/browser_history_domain_overview.ipynb`
