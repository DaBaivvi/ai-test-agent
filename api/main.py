from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from agent.models import RunRequest
from agent.graph import run_pipeline, RUN_ID
from pathlib import Path
from fastapi.responses import HTMLResponse
from markdown_it import MarkdownIt


app = FastAPI(title="AI Test Agent – PoC")

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run(req: RunRequest):
    res = run_pipeline(req)
    return res.model_dump()

md = MarkdownIt()

@app.get("/report/{run_id}/html", response_class=HTMLResponse)
def get_report_html(run_id: str):
    p = Path("reports") / f"{run_id}.md"
    if not p.exists():
        return HTMLResponse(
            "<h1>Report not found</h1>", status_code=404
        )

    markdown_text = p.read_text(encoding="utf-8")
    html_body = md.render(markdown_text)

    page = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Report – {run_id}</title>
  <style>
    body {{
      max-width: 800px;
      margin: 2rem auto;
      font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    pre, code {{
      background: #f6f8fa;
      padding: 2px 4px;
      border-radius: 4px;
      font-size: 14px;
    }}
    h1, h2, h3 {{
      font-weight: 600;
    }}
  </style>
</head>
<body>
{html_body}
</body>
</html>
"""
    return HTMLResponse(page)