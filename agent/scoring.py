from .models import Protocol, Evidence, ScoreItem, ScoreResult
from .tools import citation_builder

KEY_MAP = {
    "energy": "energy_kwh_per_cycle",
    "clean": "clean_index",
    "noise": "noise_db",
    "service": "service_score",
}

def _normalize(value: float, rule: dict) -> float:
    v = value
    if rule["scale"] == "lower_better":
        return max(0.0, min(1.0, (rule["max"] - v) / (rule["max"] - rule["min"])))
    else:
        return max(0.0, min(1.0, (v - rule["min"]) / (rule["max"] - rule["min"])) )

def compute_scores(protocol: Protocol, evidence: Evidence) -> ScoreResult:
    details = []
    total = 0.0
    warnings = []

    for c in protocol.criteria:
        mkey = KEY_MAP.get(c.id)
        if mkey not in evidence.metrics:
            warnings.append(f"missing metric for {c.id}")
            continue
        raw = evidence.metrics[mkey]
        norm = _normalize(raw, c.rule.model_dump())
        partial = norm * c.weight
        cites = [citation_builder(s.url) for s in evidence.sources]
        confidence = 0.9 if cites else 0.6
        details.append(ScoreItem(
            criterion_id=c.id,
            raw_value=raw,
            normalized=norm,
            weight=c.weight,
            partial_score=partial,
            citations=cites,
            confidence=confidence,
        ))
        total += partial

    return ScoreResult(total=round(total, 4), details=details, protocol_id=protocol.protocol_id, warnings=warnings)
