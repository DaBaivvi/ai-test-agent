AI Test Agent – Product Evaluation & Review Automation

An intelligent local-first evaluation agent that simulates a product testing pipeline.
It generates scoring details, validates them, and uses a local LLM (via Ollama) to detect anomalies and explain results in natural language.

This project is ideal for:
	•	Product testing automation
	•	Quality assurance (QA)
	•	LLM-based rule validation
	•	Local inference without cloud APIs

1. FastAPI-based agent backend
	•	/run endpoint runs a full evaluation pipeline
	•	/report/{run_id}/html renders a human-readable HTML report
	•	/health for service check

2. Modular scoring pipeline

Pipeline modules under agent/:
	•	planner – determines test protocol
	•	tools – determines which tests to run
	•	scoring – applies scoring rules
	•	guard – basic sanity checks
	•	reviewer – anomaly detection
	•	report – generates Markdown & HTML reports

3. Local LLM anomaly review (Ollama)

Uses local model (e.g., qwen2.5:1.5b-instruct) via OpenAI-compatible API:
	•	Checks for out-of-range values
	•	Detects abnormal normalized scores
	•	Finds suspicious partial scores
	•	Identifies missing criteria
	•	Generates Markdown summary

  Example output:
  ## Anomalies
  - Criterion: noise
  - Issue: raw_value=52.0 but normalized=0.0
  - Reason: Raw value extremely high → normalization loss

  ## Normal Explanation
  All other criteria fall within expected ranges.

  4. Clean Markdown + HTML Reports

  Example report screenshot:

  <img width="850" height="814" alt="Bildschirmfoto 2025-11-13 um 14 23 03" src="https://github.com/user-attachments/assets/adc79037-eeaf-4fc0-a4bf-437d108f8644" />

  Report includes:
	•	Test header
	•	Scoring details
	•	Reviewer LLM notes
	•	Anomaly section & normal explanation

  🧩 Architecture Overview
	  FastAPI
	   └── /run
	      └── agent.graph.run_pipeline()
	           ├── planner
	           ├── tools
	           ├── scoring
	           ├── guard
	           ├── reviewer (Ollama LLM)
	           └── report → Markdown / HTML
