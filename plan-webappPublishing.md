# Plan: Publish Browser History Notebook as a Web App

## Problem

The current project runs locally in Jupyter/VS Code.
Goal: let *anyone* upload their own `BrowserHistory.csv` and get the same interactive analysis — without installing Python.

---

## Option 1 — Streamlit App → Streamlit Community Cloud (Free, No Azure Required)

### What it is
Convert `browser_history_domain_overview.ipynb` into a single `app.py` Streamlit script.
Streamlit is a Python framework that turns a script into a browser UI in ~10 lines of extra code.
Host for free at **streamlit.io/cloud** (GitHub login → deploy in 3 clicks, no credit card).

### Architecture
```
User opens URL (share.streamlit.io/rs38/browser_history)
  → Streamlit Cloud runs app.py on their servers
  → User uploads CSV via st.file_uploader()
  → Pandas + Matplotlib run server-side
  → Charts rendered in browser via Streamlit's frontend
```

### How it works
1. Add `streamlit` to `pyproject.toml` (`uv add streamlit`)
2. Create `app.py` that mirrors the notebook sections:
   ```python
   import streamlit as st
   import pandas as pd

   st.title("Browser History Analysis")
   uploaded = st.file_uploader("Upload your BrowserHistory.csv", type="csv")
   if uploaded:
       df = pd.read_csv(uploaded, encoding="utf-8-sig", parse_dates=["DateTime"])
       # ... all existing analysis code ...
       st.pyplot(fig)          # show matplotlib figure
       st.dataframe(df_top)    # show table
   ```
3. Push to GitHub → go to share.streamlit.io → "New app" → select repo

### Pros
- ✅ **Easiest migration** — existing pandas/matplotlib code works unchanged
- ✅ **Free tier** is generous for a personal tool
- ✅ **No Azure, no Docker, no CI** needed
- ✅ CSV never leaves the server session (privacy-reasonable)
- ✅ Works on mobile

### Cons
- ❌ Server is shared/slow on free tier (cold start ~30 s)
- ❌ CSV is processed on Streamlit's US servers (privacy concern for sensitive history)
- ❌ Requires an active server — app sleeps after inactivity

### Cost
**Free** on Streamlit Community Cloud for public repos.
If you need private repos or always-on: ~$10/mo (Streamlit Teams) or host on Azure App Service Basic (~€12/mo) / Railway (~$5/mo).

---

## Option 2 — JupyterLite on GitHub Pages (100 % Static, WASM, Free)

### What it is
**JupyterLite** is a full Jupyter environment that runs entirely in the browser via **Pyodide** (Python compiled to WebAssembly).
No server. No Python installation. GitHub Pages serves only static files.
The user's CSV never leaves their machine — everything runs client-side.

### Architecture
```
User opens https://rs38.github.io/browser_history
  → GitHub Pages serves static HTML/JS/WASM files
  → Browser downloads Pyodide (~10 MB, cached)
  → User uploads CSV via JupyterLite UI
  → Pandas/Matplotlib run inside the browser (WebAssembly)
  → Charts rendered in-browser
```

### How it works
1. Add a GitHub Actions workflow that builds a JupyterLite site:
   ```yaml
   # .github/workflows/deploy.yml
   - uses: actions/checkout@v4
   - run: pip install jupyterlite-core jupyterlite-pyodide-kernel
   - run: jupyter lite build --contents browser_history_domain_overview.ipynb --output-dir dist
   - uses: actions/deploy-pages@v4
   ```
2. Enable GitHub Pages on the repo (Settings → Pages → "GitHub Actions")
3. Done — notebook opens at `https://rs38.github.io/browser_history`

### Supported packages (via Pyodide)
`pandas`, `matplotlib`, `numpy`, `scipy` — all already available in Pyodide.
`scikit-learn` also available if needed for the ML phase.

### Pros
- ✅ **100 % free forever** — GitHub Pages has no usage limits for static files
- ✅ **Privacy-first** — CSV processed entirely in the user's browser, never uploaded
- ✅ **No server to maintain** — zero ops
- ✅ **Works with the existing notebook** — minimal changes needed
- ✅ Pure WASM — what the problem statement directly asks about

### Cons
- ❌ First load is slow (~10–30 s to download Pyodide + packages)
- ❌ Browser memory limit (~2 GB) — fine for typical browser history CSVs
- ❌ Notebook UI (Jupyter) is less polished than Streamlit for end-users
- ❌ Some packages (e.g. `sentence-transformers`) not yet in Pyodide

### Cost
**Free** — GitHub Pages + GitHub Actions free tier covers this easily.

---

## Option 3 — Marimo Reactive Notebook → GitHub Pages (WASM, Modern UX)

### What it is
**Marimo** is a next-generation Python notebook that:
- Runs as a reactive app (cells re-execute automatically when inputs change)
- Can be compiled to a **self-contained WASM bundle** (`marimo export html`)
- Deployed as a static HTML file on GitHub Pages — no server

This gives a polished app-like UI while staying 100 % static.

### Architecture
```
User opens https://rs38.github.io/browser_history/app.html
  → Single HTML file (with embedded WASM runtime) loads
  → User uploads CSV via a file-picker widget
  → Python runs in-browser via Pyodide
  → Charts update reactively as user changes filters/sliders
```

### How it works
1. Install Marimo: `uv add marimo`
2. Convert the notebook logic to a Marimo app (`app.py`):
   ```python
   import marimo as mo
   import pandas as pd

   file = mo.ui.file(label="Upload BrowserHistory.csv")

   @mo.cell
   def _(file):
       if file.value:
           df = pd.read_csv(file.value[0].contents, encoding="utf-8-sig")
           return mo.ui.table(df.head(20))
   ```
3. Export to static HTML:
   ```bash
   marimo export html app.py -o dist/app.html
   ```
4. Deploy via GitHub Actions to GitHub Pages (same pattern as Option 2)

### Pros
- ✅ **Best UX** — reactive sliders/dropdowns feel like a real app
- ✅ **100 % static + privacy-first** — runs entirely in browser via WASM
- ✅ **Single HTML file** — trivially shareable (email, Gist, Dropbox link)
- ✅ **Free forever** on GitHub Pages
- ✅ Modern Python notebook standard — better than classic Jupyter for apps

### Cons
- ❌ Requires rewriting the notebook in Marimo syntax (1–3 hours)
- ❌ Still uses Pyodide — same ~10–30 s first-load time
- ❌ Marimo is newer — smaller community than Streamlit

### Cost
**Free** — GitHub Pages + GitHub Actions free tier.

---

## Summary & Recommendation

| | Option 1: Streamlit | Option 2: JupyterLite | Option 3: Marimo WASM |
|---|---|---|---|
| **Hosting** | Streamlit Cloud / Azure | GitHub Pages (static) | GitHub Pages (static) |
| **Cost** | Free (public) | Free | Free |
| **Privacy** | CSV on server | CSV stays in browser | CSV stays in browser |
| **Effort** | Low (1–2 h) | Very low (30 min) | Medium (2–4 h) |
| **UX quality** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **No Azure needed** | ✅ | ✅ | ✅ |
| **Pure WASM** | ❌ | ✅ | ✅ |

**Quickest win:** Option 2 (JupyterLite) — existing notebook works almost unchanged, deployed in 30 minutes via GitHub Actions, free and private.

**Best long-term UX:** Option 3 (Marimo) — feels like a real app, still static/free/private, but requires rewriting in Marimo syntax.

**Best if you want an interactive polished tool fast:** Option 1 (Streamlit) — minimal code changes, excellent widget ecosystem, no WASM limitations.

> **Azure is not needed for any of these options.** All three run entirely on free-tier infrastructure. Azure App Service would only make sense if you need enterprise features (custom domain, SLA, always-on, private VNet) — which is overkill for a personal analysis tool.
