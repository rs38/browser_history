from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

DEFAULT_CSV_PATH = Path("BrowserHistory_22.02.26.csv")


def extract_domain(url: str) -> str:
    if not url:
        return "(empty)"

    parsed = urlparse(url)
    domain = parsed.netloc.lower().strip()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain or "(no-domain)"


def load_history_df(csv_path: Path = DEFAULT_CSV_PATH) -> pd.DataFrame:
    df = pd.read_csv(
        csv_path,
        encoding="utf-8-sig",
        parse_dates=["DateTime"],
        index_col="DateTime",
    )

    df["domain"] = df["NavigatedToUrl"].apply(extract_domain)
    return df
