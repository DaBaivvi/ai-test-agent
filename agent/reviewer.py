from typing import List
from .models import ScoreResult
from .llm import hf_review

#def review(scores: ScoreResult) -> List[str]:
#    notes: List[str] = []
#    computed = round(sum(d.partial_score for d in scores.details), 4)
#   if abs(computed - scores.total) > 1e-4:
#        notes.append("score mismatch")
 #   if len(scores.details) < 3:
  #      notes.append("insufficient coverage: <3 criteria")
   # return notes

def review(scores: ScoreResult) -> List[str]:
    notes: List[str] = []
    computed = round(sum(d.partial_score for d in scores.details), 4)
    if abs(computed - scores.total) > 1e-4:
        notes.append("score mismatch")
    if len(scores.details) < 3:
        notes.append("insufficient coverage: <3 criteria>")

    
    try:
        details = [d.model_dump() for d in scores.details]
        result = hf_review(scores.protocol_id, details)
        notes.append(f"LLM summary: {result['summary']}")
    except Exception as e:
        notes.append(f"hf_review_failed: {e}")

    return notes