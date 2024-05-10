.PHONY: install virtualenv ipython clean test watch pflake8


install:
	@echo "Installing for dev environment"
	@.venv/bin/python -m pip install -e '.[dev]'


virtualenv:
	@python -m venv .venv
	@source .venv/bin/activate

ipython:
	@.venv/bin/ipython

lint:
	@.venv/bin/pflake8

fmt:
	@.venv/bin/isort dundie tests integration
	@.venv/bin/black dundie tests integration

test:
	@.venv/bin/pytest -s --forked

testci:
	@pytest -v --junitxml=test-result.xml

watch:
	#@.venv/bin/ptw
	@ls **/*.py | entr pytest --forked

clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
