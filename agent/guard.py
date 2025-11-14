from typing import List
from .models import Evidence, ScoreResult
from .tools import is_fresh

WHITELIST = {"official", "internal"}

def compliance_check(ev: Evidence, scores: ScoreResult) -> List[str]:
    flags: List[str] = []
    for s in ev.sources:
        if s.type not in WHITELIST:
            flags.append(f"source not allowed: {s.id}")
        if not is_fresh(s.fetched_at, days=540):
            flags.append(f"stale evidence: {s.id}")
    for d in scores.details:
        if d.confidence < 0.7:
            flags.append(f"low confidence on {d.criterion_id}")
    return flags
