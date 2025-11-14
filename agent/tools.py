import json, hashlib, re, datetime
from pathlib import Path
from typing import Tuple, Dict
from .models import Protocol, Evidence

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def retrieve_protocol(category: str) -> Protocol:
    p = DATA_DIR / "protocols" / "waschmaschine.v1.json"
    return Protocol(**json.loads(p.read_text(encoding="utf-8")))

def fetch_evidence(category: str, model: str) -> Evidence:
    p = DATA_DIR / "evidences" / "sample_wm_xz500.json"
    return Evidence(**json.loads(p.read_text(encoding="utf-8")))

def privacy_filter(text: str) -> str:
    text = re.sub(r"\b\d{2,4}-\d{2,4}-\d{2,4}\b", "[MASKED]", text)
    return text

def citation_builder(url: str) -> str:
    h = hashlib.sha1(url.encode()).hexdigest()[:8]
    return f"cite:{h}"

def is_fresh(iso_date: str, days: int = 365) -> bool:
    dt = datetime.date.fromisoformat(iso_date)
    return (datetime.date.today() - dt).days <= days
