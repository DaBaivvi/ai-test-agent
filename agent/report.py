import json
from pathlib import Path
from .models import ScoreResult, RunRequest

REPORTS = Path("reports")
REPORTS.mkdir(exist_ok=True)

def save_report(run_id: str, req: RunRequest, scores: ScoreResult, flags: list, reviews: list) -> str:
    md = [
        f"# Testbericht – {req.category} / {req.model}",
        f"Protocol: {scores.protocol_id}",
        f"Gesamtscore: **{scores.total:.3f}**\n",
        "## Details",
    ]
    for d in scores.details:
        md.append(f"- {d.criterion_id}: raw={d.raw_value} norm={d.normalized:.3f} weight={d.weight} partial={d.partial_score:.3f}")
        md.append(f"  citations: {', '.join(d.citations)} | conf={d.confidence}")
    if flags:
        md.append("\n## Compliance Flags\n- " + "\n- ".join(flags))
    if reviews:
        md.append("\n## Reviewer Notes\n- " + "\n- ".join(reviews))

    out = REPORTS / f"{run_id}.md"
    out.write_text("\n".join(md), encoding="utf-8")

    j = REPORTS / f"{run_id}.json"
    j.write_text(json.dumps(scores.model_dump(), indent=2), encoding="utf-8")
    return str(out)
