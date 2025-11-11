test:
	pytest tests

format:
	ruff format .
	ruff check --fix .

checkformat:
	ruff format --check .
	ruff check .

checktodo:
	(find . -name "*.py" | grep -v "/\." | xargs grep -l "TODO") && echo "TODOs found" && exit 1 || echo "No TODOs found" && exit 0

# Type checking with mypy
mypy:
	mypy fakephylo --config-file pyproject.toml

# Run all code quality checks
check: checktodo mypy checkformat
	@echo "✅ All code quality checks passed!"

.PHONY: test format check checkformat checktodo mypy
