.PHONY: format lint test
format:
	pre-commit run --all-files || true
lint:
	ruff src tests
test:
	pytest -q
