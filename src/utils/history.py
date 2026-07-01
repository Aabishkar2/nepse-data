import math
import pandas as pd

_FLOAT_COLS = ["open", "high", "low", "close", "per_change",
               "traded_quantity", "traded_amount"]
_ORDER = ["published_date"] + _FLOAT_COLS + ["status"]


class AuthError(Exception):
    """Raised when the history API returns an error body (e.g. CSRF mismatch)
    instead of a valid DataTables response. Signals the caller to refresh the
    session token and retry."""


def records_total(resp_json):
    """Return recordsTotal from a history-API response, or raise AuthError if
    the response is an error payload (no recordsTotal — e.g. CSRF mismatch,
    which the server returns as HTTP 200 with a 'message')."""
    if "recordsTotal" not in resp_json:
        raise AuthError(resp_json.get("message", "missing recordsTotal"))
    return resp_json["recordsTotal"]


def page_starts(total, size):
    pages = math.ceil(total / size)
    return [i * size for i in range(pages)]


def records_to_dataframe(records):
    df = pd.DataFrame.from_dict(records)
    if "DT_Row_Index" in df.columns:
        df = df.drop(columns="DT_Row_Index")
    df = df[::-1].reset_index(drop=True)
    for col in _FLOAT_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["status"] = df["status"].astype(int)
    return df[_ORDER]
