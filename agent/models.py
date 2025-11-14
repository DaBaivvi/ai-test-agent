from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ProtocolRule(BaseModel):
    scale: str  # "higher_better" | "lower_better"
    min: float
    max: float

class Criterion(BaseModel):
    id: str
    name: str
    weight: float = Field(ge=0, le=1)
    rule: ProtocolRule

class Protocol(BaseModel):
    protocol_id: str
    category: str
    version: int
    criteria: List[Criterion]

class EvidenceSource(BaseModel):
    id: str
    type: str  # official/internal/vendor
    url: str
    hash: str
    fetched_at: str  # ISO date

class Evidence(BaseModel):
    category: str
    model: str
    sources: List[EvidenceSource]
    metrics: Dict[str, float]

class Plan(BaseModel):
    tasks: List[str]
    notes: Optional[str] = None

class ScoreItem(BaseModel):
    criterion_id: str
    raw_value: float
    normalized: float
    weight: float
    partial_score: float
    citations: List[str]
    confidence: float

class ScoreResult(BaseModel):
    total: float
    details: List[ScoreItem]
    protocol_id: str
    warnings: List[str] = []

class RunRequest(BaseModel):
    category: str
    model: str

class RunResult(BaseModel):
    run_id: str
    protocol_id: str
    score_total: float
    report_path: str
    warnings: List[str]
