from .models import Plan, RunRequest

def make_plan(req: RunRequest) -> Plan:
    tasks = [
        "load_protocol",
        "collect_evidence",
        "score_compute",
        "compliance_guard",
        "review",
        "build_report",
    ]
    notes = f"Category={req.category}; Model={req.model}"
    return Plan(tasks=tasks, notes=notes)
