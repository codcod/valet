.PHONY = venv check test venv-devel

export PYTHONPATH=.

venv:
	python -m venv .venv
	( bash -c "source .venv/bin/activate && python -m pip install --upgrade pip setuptools wheel"; )
	( bash -c "source .venv/bin/activate && pip install -r requirements/prod.txt"; )
	@printf "\nDone. You can now activate the virtual environment:\n  source .venv/bin/activate\n"

venv-devel: venv
	( bash -c "source .venv/bin/activate && pip install -r requirements/devel.txt"; )
	

check:
	mypy --strict --scripts-are-modules --implicit-reexport valet
		#scripts/*

test:
	pytest  # configured via pyproject.toml
