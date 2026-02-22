# Browser History Analysis - AI Coding Guidelines

## Project Overview
This is a data analysis project for browser history visualization and insights. The codebase uses Jupyter notebooks with standard Python libraries organized into incremental analysis sections.

## Dependency Management
- Use **`uv add <package>`** instead of `pip install` for adding dependencies
- Current stack: **pandas** for data handling, numpy (pandas dependency)
- For visualizations, use `uv add plotly` or `uv add matplotlib`

## CSV & Data Handling Patterns
- **Load with pandas:** Use `pd.read_csv(encoding="utf-8-sig")` to handle Windows browser CSV exports with UTF-8 BOM
- **DateTime as index:** Always set `parse_dates=["DateTime"], index_col="DateTime"` when loading history CSV to enable time-based filtering
- **Column operations:** Use `.apply()` for element-wise transformations (e.g., domain extraction)
- **Aggregation:** Use `.value_counts()` for frequency counts, not manual Counter objects
- Example: [CSV loading in browser_history_domain_overview.ipynb](../browser_history_domain_overview.ipynb)

## Domain Extraction & Analysis
- Normalize domains using `urllib.parse.urlparse()` + `.netloc.lower()` 
- Strip leading `www.` prefix to unify domain buckets
- Handle edge cases: empty URLs → `"(empty)"`, missing domain → `"(no-domain)"`
- Apply domain extraction via `df["domain"] = df["NavigatedToUrl"].apply(extract_domain)`
- Frequency analysis via pandas `.value_counts()` returns sorted Series automatically
- Example: [extract_domain function](../browser_history_domain_overview.ipynb)

## Notebook Structure
- Use **section headers** (`## 1) ...`, `## 2) ...`) to organize incremental analysis steps
- Lead each section with a **markdown description** of what the code cell does
- Each cell should have a single responsibility: load, transform, analyze, visualize
- Keep outputs human-readable with formatting: `f"{value:,}"` for thousands separators, aligned columns

## Working Directory
- Assume notebooks run from the workspace root: `d:\source\browser_history\`
- Path references use `Path()` for cross-platform compatibility

## Google Search Parameter Patterns
- **AI Overview detection:** `udm=50` parameter indicates Google's AI-powered search result (formerly SGE - Search Generative Experience)
- **Query extraction:** Use `parse_qs()` to extract `q` parameter and decode `+` to spaces
- Extract using `urlparse()` + `parse_qs()` for robust URL parsing
- Example: Filter `df[df["has_ai_overview"]]` to isolate AI-assisted searches

## Search Topic Classification
- Classify queries using keyword matching across predefined topic categories
- Categories: AI/ML, Programming, Hardware/Electronics, Automotive/Vehicles, Shopping/Ecommerce, General Info, Tools/Utilities, News/Current
- Use case-insensitive keyword matching: `if keyword in query.lower()`
- Assign default category "Other" for queries matching multiple categories or none
- Example: [Topic classifier function](../browser_history_domain_overview.ipynb)

## Extending This Project
- New analysis sections belong in the same notebook with new numbered sections
- If adding external data viz (e.g., domain trends over time), consider `uv add plotly` or `uv add matplotlib`
- Keep domain extraction logic reusable; consider refactoring to a shared module if >2 analysis notebooks exist
