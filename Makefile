.PHONY: install lint test rehearse ci install-workflow

install:
	python -m pip install --upgrade pip
	python -m pip install -e .[dev]

lint:
	ruff check .

test:
	pytest

rehearse:
	python -m rolex_reservation_assistant rehearse --profile config/applicant.example.json --location all --selectors config/selectors.mock.json --iterations 100

ci:
	python ci/run_ci.py

install-workflow:
	python scripts/install_github_actions_workflow.py
