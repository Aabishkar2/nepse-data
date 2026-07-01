import re
import requests
from config.headers import headers

_TOKEN_RE = re.compile(r'name="_token"\s+value="([^"]+)"')
_COMPANYID_RE = re.compile(r'id="companyid"[^>]*>\s*([0-9]+)')
_SYMBOL_RE = re.compile(r'id="symbol"[^>]*>\s*([A-Za-z0-9]+)')

BASE = "https://www.sharesansar.com"
TIMEOUT = 30  # seconds; a throttled server may hold the connection open


def extract_token(html):
    m = _TOKEN_RE.search(html)
    return m.group(1) if m else None


def extract_companyid(html):
    m = _COMPANYID_RE.search(html)
    return m.group(1) if m else None


def extract_symbol(html):
    m = _SYMBOL_RE.search(html)
    return m.group(1) if m else None


def make_session():
    session = requests.Session()
    session.headers.update(headers)
    return session


def prime_session(session, symbol="adbl"):
    resp = session.get(f"{BASE}/company/{symbol.lower()}", timeout=TIMEOUT)
    resp.raise_for_status()
    return extract_token(resp.text)
