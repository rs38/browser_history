from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

DEFAULT_CSV_PATH = Path("BrowserHistory.csv")


def extract_domain(url: str) -> str:
    if not url:
        return "(empty)"

    parsed = urlparse(url)
    domain = parsed.netloc.lower().strip()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain or "(no-domain)"


def _auto_detect_csv() -> Path:
    """Return the most recently modified CSV in the working directory."""
    candidates = sorted(Path(".").glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise FileNotFoundError(
            "No CSV file found in the working directory. "
            "Upload your browser history CSV via the file-upload widget or place it here."
        )
    return candidates[0]


def _extract_upload(uploader) -> tuple[str, bytes] | None:
    """Return (filename, raw_bytes) from a FileUpload widget, or None if empty.

    Handles both ipywidgets v7 (dict) and v8+ (tuple) value formats.
    """
    val = getattr(uploader, "value", None)
    if not val:
        return None
    # v8+: value is a tuple of dicts with keys "name", "content", ...
    if isinstance(val, tuple):
        item = val[0]
        return item["name"], bytes(item["content"])
    # v7: value is a dict keyed by filename
    fname, meta = next(iter(val.items()))
    return fname, bytes(meta["content"])


def _save_upload_to_disk(uploader) -> Path | None:
    """Write the widget's uploaded file to the current working directory.

    Returns the Path it was saved to, or None if the widget is empty.
    """
    result = _extract_upload(uploader)
    if result is None:
        return None
    fname, raw = result
    dest = Path(fname)
    dest.write_bytes(raw)
    return dest


def make_upload_widget():
    """Return an ipywidgets FileUpload widget pre-configured for CSV files.

    The widget automatically saves the uploaded file to the notebook working
    directory on upload, so it persists across kernel restarts.  A status
    Output widget is stacked below the button; any save errors are shown
    there rather than silently swallowed (a common pitfall in classic Jupyter).

    Usage in a notebook cell::

        uploader = make_upload_widget()
        display(uploader)

    Then in a later cell::

        df = load_history_df(uploader=uploader)
    """
    import ipywidgets as widgets  # optional dep; only needed in notebook

    w = widgets.FileUpload(accept=".csv", multiple=False, description="Upload CSV")
    out = widgets.Output()

    def _on_upload(change):
        with out:
            out.clear_output()
            try:
                saved = _save_upload_to_disk(w)
                if saved:
                    print(f"✅ Saved to working directory: {saved}")
            except Exception as exc:
                print(f"❌ Failed to save file: {exc}")

    w.observe(_on_upload, names="value")
    display(widgets.VBox([w, out]))
    # Return the FileUpload widget so callers can pass it to load_history_df()
    return w


def load_history_df(
    csv_path: Path | None = None,
    *,
    uploader=None,
) -> pd.DataFrame:
    """Load a browser-history CSV into a DataFrame.

    Priority:
    1. ``uploader`` – an ipywidgets FileUpload widget that already has a file.
       The file is also written to disk so it survives a kernel restart.
    2. ``csv_path``  – an explicit Path (falls back to DEFAULT_CSV_PATH if not given).
    3. Auto-detect   – picks the most recently modified ``*.csv`` in the CWD.
    """
    if uploader is not None:
        result = _extract_upload(uploader)
        if result is not None:
            fname, raw = result
            # Persist to disk (idempotent if make_upload_widget already did it)
            Path(fname).write_bytes(raw)
            df = pd.read_csv(
                BytesIO(raw),
                encoding="utf-8-sig",
                parse_dates=["DateTime"],
                index_col="DateTime",
            )
            df["domain"] = df["NavigatedToUrl"].apply(extract_domain)
            return df

    if csv_path is None:
        csv_path = DEFAULT_CSV_PATH if DEFAULT_CSV_PATH.exists() else _auto_detect_csv()
    df = pd.read_csv(
        csv_path,
        encoding="utf-8-sig",
        parse_dates=["DateTime"],
        index_col="DateTime",
    )
    df["domain"] = df["NavigatedToUrl"].apply(extract_domain)
    return df


# ---------------------------------------------------------------------------
# Topic classification
# ---------------------------------------------------------------------------

DOMAIN_CATEGORY_MAP: dict[str, str] = {
    # Programming
    "github.com": "Programming",
    "stackoverflow.com": "Programming",
    "gitlab.com": "Programming",
    "bitbucket.org": "Programming",
    "python.org": "Python",
    "pypi.org": "Python",
    "nodejs.org": "JavaScript/Web",
    "npmjs.com": "JavaScript/Web",
    "reactjs.org": "JavaScript/Web",
    "vuejs.org": "JavaScript/Web",
    "rust-lang.org": "Systems/Backend",
    "go.dev": "Systems/Backend",
    "docs.microsoft.com": "Programming",
    "learn.microsoft.com": "Programming",
    "developer.mozilla.org": "JavaScript/Web",
    "w3schools.com": "JavaScript/Web",
    "hub.docker.com": "Systems/Backend",
    "docker.com": "Systems/Backend",
    # AI / ML
    "openai.com": "AI/LLMs",
    "chat.openai.com": "AI/LLMs",
    "claude.ai": "AI/LLMs",
    "huggingface.co": "ML/Deep Learning",
    "tensorflow.org": "ML/Deep Learning",
    "pytorch.org": "ML/Deep Learning",
    "kaggle.com": "Data Science",
    "deepseek.com": "AI/LLMs",
    "chat.deepseek.com": "AI/LLMs",
    "perplexity.ai": "AI/LLMs",
    "copilot.microsoft.com": "AI/LLMs",
    # Entertainment
    "youtube.com": "Entertainment/Media",
    "netflix.com": "Entertainment/Media",
    "twitch.tv": "Entertainment/Media",
    "imdb.com": "Entertainment/Media",
    "spotify.com": "Entertainment/Media",
    "reddit.com": "Entertainment/Media",
    "tiktok.com": "Entertainment/Media",
    "instagram.com": "Entertainment/Media",
    "facebook.com": "Entertainment/Media",
    "twitter.com": "Entertainment/Media",
    "x.com": "Entertainment/Media",
    "primevideo.com": "Entertainment/Media",
    "disneyplus.com": "Entertainment/Media",
    "store.steampowered.com": "Entertainment/Media",
    "steampowered.com": "Entertainment/Media",
    # Shopping
    "amazon.com": "Shopping/Ecommerce",
    "amazon.de": "Shopping/Ecommerce",
    "ebay.com": "Shopping/Ecommerce",
    "ebay.de": "Shopping/Ecommerce",
    "aliexpress.com": "Shopping/Ecommerce",
    "etsy.com": "Shopping/Ecommerce",
    "otto.de": "Shopping/Ecommerce",
    "zalando.de": "Shopping/Ecommerce",
    "mediamarkt.de": "Shopping/Ecommerce",
    "idealo.de": "Shopping/Ecommerce",
    "geizhals.de": "Shopping/Ecommerce",
    "conrad.de": "Shopping/Ecommerce",
    # News
    "bbc.com": "News/Current",
    "cnn.com": "News/Current",
    "dw.com": "News/Current",
    "spiegel.de": "News/Current",
    "zeit.de": "News/Current",
    "heise.de": "News/Current",
    "golem.de": "News/Current",
    "ard.de": "News/Current",
    "tagesschau.de": "News/Current",
    "sueddeutsche.de": "News/Current",
    "faz.net": "News/Current",
    # Travel
    "booking.com": "Travel/Location",
    "airbnb.com": "Travel/Location",
    "expedia.com": "Travel/Location",
    "tripadvisor.com": "Travel/Location",
    "maps.google.com": "Travel/Location",
    "openstreetmap.org": "Travel/Location",
    "flightradar24.com": "Travel/Location",
    # Finance
    "coinbase.com": "Finance/Investment",
    "crypto.com": "Finance/Investment",
    "investing.com": "Finance/Investment",
    "coingecko.com": "Finance/Investment",
    "binance.com": "Finance/Investment",
    "tradingview.com": "Finance/Investment",
    "finanzen.net": "Finance/Investment",
    # Work
    "linkedin.com": "Work/Career",
    "indeed.com": "Work/Career",
    "xing.com": "Work/Career",
    # Health
    "webmd.com": "Health/Medical",
    "mayoclinic.org": "Health/Medical",
    "healthline.com": "Health/Medical",
    "netdoktor.de": "Health/Medical",
    # Education
    "udemy.com": "Education/Learning",
    "coursera.org": "Education/Learning",
    "edx.org": "Education/Learning",
    "khanacademy.org": "Education/Learning",
    "codecademy.com": "Education/Learning",
    "wikipedia.org": "General Info",
    # Tools / Utilities
    "notion.so": "Tools/Utilities",
    "trello.com": "Tools/Utilities",
    "figma.com": "Tools/Utilities",
    "canva.com": "Tools/Utilities",
    "obsidian.md": "Tools/Utilities",
}

TOPICS: dict[str, list[str]] = {
    "Python": [
        "python", "django", "flask", "pip", "pandas", "numpy", "jupyter",
        "anaconda", "virtualenv", "pycharm", "pytest", "poetry", "fastapi",
        "sqlalchemy", "python-programmierung", "pythonista",
    ],
    "JavaScript/Web": [
        "javascript", "react", "nodejs", "node.js", "typescript", "html",
        "css", "vue", "angular", "npm", "webpack", "vite", "svelte",
        "next.js", "nuxt", "tailwind", "bootstrap", "frontend",
        "web development", "webentwicklung",
    ],
    "Systems/Backend": [
        "rust", "golang", "c++", "c#", "java", "kotlin", "backend",
        "microservice", "postgresql", "mysql", "redis", "docker",
        "kubernetes", "devops", "linux", "systemd", "datenbank",
    ],
    "Mobile Dev": [
        "swift", "ios", "android", "flutter", "react native",
        "xcode", "android studio", "app development", "mobilentwicklung",
    ],
    "AI/LLMs": [
        "copilot", "agent", "gpt", "llm", "chatgpt", "openai", "claude",
        "deepseek", "prompt", "gemini", "mistral", "ollama", "rag",
        "langchain", "llama", "mcp", "whisper", "ki", "chatbot",
        "sprachmodell", "kuenstliche intelligenz",
    ],
    "Data Science": [
        "data science", "data analysis", "visualization", "tableau",
        "power bi", "seaborn", "plotly", "notebook", "statistics",
        "regression", "datenanalyse", "datenwissenschaft",
    ],
    "ML/Deep Learning": [
        "neural", "deep learning", "tensorflow", "pytorch", "keras",
        "scikit", "sklearn", "reinforcement", "transformer", "fine-tuning",
        "embedding", "maschinelles lernen", "neuronales netz",
    ],
    "Hardware/Electronics": [
        "arduino", "raspberry", "circuit", "usb", "microcontroller",
        "fnirsi", "multimeter", "instek", "breadboard", "sensor",
        "electronics", "pcb", "soldering", "oscilloscope", "embedded",
        "schematic", "platine", "loetkolben", "widerstand",
    ],
    "Automotive/Vehicles": [
        "mercedes", "volvo", "bmw", "audi", "volkswagen", "toyota",
        "automobile", "engine", "motor", "vehicle", "driving", "repair",
        "maintenance", "fuel", "tire", "tesla", "electric vehicle",
        "auto", "kfz", "fahrzeug", "reparatur", "wartung",
    ],
    "Health/Medical": [
        "health", "medical", "disease", "symptom", "doctor", "treatment",
        "medication", "hospital", "therapy", "wellness", "exercise",
        "nutrition", "mental health", "anxiety", "depression", "fitness",
        "gesundheit", "arzt", "krankheit", "medikament", "behandlung",
        "ernaehrung",
    ],
    "Entertainment/Media": [
        "movie", "film", "show", "gaming", "stream",
        "actor", "imdb", "music", "song", "artist", "album", "concert",
        "anime", "manga", "podcast", "serie", "musik", "spiel",
    ],
    "Travel/Location": [
        "hotel", "flight", "airport", "booking", "vacation", "travel",
        "route", "directions", "tourism", "hostel", "resort", "ticket",
        "reise", "urlaub", "flug", "stadtplan",
    ],
    "Finance/Investment": [
        "stock", "crypto", "bitcoin", "finance", "investment", "bank",
        "loan", "mortgage", "insurance", "tax", "savings", "trading",
        "portfolio", "ethereum", "defi",
        "aktie", "finanzen", "investition", "steuer", "versicherung",
        "krypto", "ersparnisse",
    ],
    "Sports": [
        "league", "football", "basketball", "soccer", "tennis",
        "championship", "tournament", "bundesliga", "formula 1", "f1",
        "cycling", "marathon", "fussball", "spieler", "mannschaft", "liga",
    ],
    "Food/Cooking": [
        "recipe", "cook", "food", "restaurant", "ingredient", "cooking",
        "baking", "cuisine", "dish", "menu", "delivery", "cafe", "vegan",
        "rezept", "kochen", "essen", "zutaten", "backen", "gericht",
    ],
    "Work/Career": [
        "resume", "interview", "salary", "employment", "career",
        "business", "company", "hiring", "recruit", "freelance", "startup",
        "bewerbung", "gehalt", "unternehmen", "karriere",
    ],
    "Education/Learning": [
        "tutorial", "learn", "class", "school", "university",
        "degree", "textbook", "exam", "study", "certification",
        "udemy", "coursera", "lecture",
        "kurs", "lernen", "schule", "studium", "pruefung", "zertifikat",
    ],
    "Shopping/Ecommerce": [
        "amazon", "ebay", "shop", "buy", "price", "product", "sale",
        "aliexpress", "store", "deal", "coupon", "discount", "purchase",
        "checkout", "retail",
        "kaufen", "preis", "angebot", "rabatt", "einkaufen",
    ],
    "News/Current": [
        "news", "breaking", "update", "announced", "release", "launched",
        "latest", "announcement", "bulletin",
        "nachrichten", "aktuell", "meldung", "bericht",
    ],
    "Tools/Utilities": [
        "tool", "utility", "software", "application", "extension",
        "download", "installer", "plugin", "addon", "script", "cli",
        "command line", "terminal", "editor", "ide",
        "werkzeug", "programm", "herunterladen",
    ],
    "General Info": [
        "what is", "how to", "why", "explain", "definition", "meaning",
        " vs ", "comparison", "guide", "understand",
        "was ist", "wie", "warum", "erklaerung", "bedeutung", "vergleich",
        "anleitung",
    ],
}


def _match_keywords(text: str) -> str:
    """Return the first matching TOPICS category, or 'Other'."""
    if not text:
        return "Other"
    text_lower = text.lower()
    for topic, keywords in TOPICS.items():
        for kw in keywords:
            if kw in text_lower:
                return topic
    return "Other"


def classify_visit(url: str, domain: str, page_title: str = "") -> str:
    """Classify a single browser visit using priority-based matching.

    Priority:
    1. Domain mapping (DOMAIN_CATEGORY_MAP)
    2. Page title keywords
    3. Domain name keywords
    4. Full URL (last resort)
    """
    url = url if isinstance(url, str) else ""
    domain = domain if isinstance(domain, str) else ""
    page_title = page_title if isinstance(page_title, str) else ""

    if domain in DOMAIN_CATEGORY_MAP:
        return DOMAIN_CATEGORY_MAP[domain]
    result = _match_keywords(page_title)
    if result != "Other":
        return result
    result = _match_keywords(domain)
    if result != "Other":
        return result
    return _match_keywords(url)


def classify_df(df: pd.DataFrame) -> pd.DataFrame:
    """Add a ``category`` column to *df* in-place and return it.

    Uses :func:`classify_visit` on every row.  Looks for an optional
    ``PageTitle`` column for better accuracy.
    """
    page_title_col = "PageTitle" if "PageTitle" in df.columns else None

    df["category"] = df.apply(
        lambda row: classify_visit(
            row["NavigatedToUrl"] if pd.notna(row["NavigatedToUrl"]) else "",
            row["domain"] if pd.notna(row["domain"]) else "",
            row[page_title_col] if (page_title_col and pd.notna(row[page_title_col])) else "",
        ),
        axis=1,
    )
    return df
