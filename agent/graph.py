from .models import RunRequest, RunResult
from . import planner, tools, scoring, guard, reviewer, report

RUN_ID = "demo-xz500"

def run_pipeline(req: RunRequest) -> RunResult:
    plan = planner.make_plan(req)

    protocol = tools.retrieve_protocol(req.category)
    evidence = tools.fetch_evidence(req.category, req.model)

    scores = scoring.compute_scores(protocol, evidence)
    flags = guard.compliance_check(evidence, scores)
    notes = reviewer.review(scores)

    path = report.save_report(RUN_ID, req, scores, flags, notes)

    return RunResult(
        run_id=RUN_ID,
        protocol_id=protocol.protocol_id,
        score_total=scores.total,
        report_path=path,
        warnings=list(set(scores.warnings + flags + notes)),
    )
