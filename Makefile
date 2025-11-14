.PHONY: run fmt lint test
run:
	PYTHONPATH="$$PWD" python -m uvicorn api.main:app --reload --port 8000
fmt:
	python -m pip install ruff==0.6.9
	ruff format
lint:
	ruff check --fix
test:
	pytest -q
