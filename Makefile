.PHONY: install virtualenv ipython enable-debugging clean test watch pflake8

install:
	@echo "Installing for dev environment"
	@.venv/bin/python -m pip install -e '.[dev]'

install-dev:
	@.venv/bin/python -m pip install -r requirements.dev.txt

install-test:
	@.venv/bin/python -m pip install -r requirements.test.txt

virtualenv:
	@python -m venv .venv
	@python -m pip install --upgrade pip

ipython:
	@.venv/bin/ipython

enable-debugging:
	@export PYTHONBREAKPOINT=ipdb.set_trace  

lint:
	@.venv/bin/pflake8

fmt:
	@.venv/bin/isort cat-weather-bot tests integration
	@.venv/bin/black cat-weather-bot tests integration

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
