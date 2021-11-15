.PHONY: dist clean qa test dev nodev todos install docs test_deps

clean:
	rm -rf carnival.egg-info dist build __pycache__ .mypy_cache .pytest_cache .coverage

test_deps:
	poetry install --no-root

qa:
	poetry run flake8 .
	poetry run mypy .

test: qa docs test_deps
	poetry run python3 -m pytest -x --cov-report term --cov=carnival -vv tests/

test_fast:
	poetry run python3 -m pytest -x --cov-report term --cov=carnival -vv -m "not slow" tests/

test_local:
	poetry run python3 -m pytest -x --cov-report term --cov=carnival -vv -m "not remote" tests/

dev:
	docker-compose -f testdata/docker-compose.yml up --build -d --remove-orphans --force-recreate

nodev:
	docker-compose -f testdata/docker-compose.yml rm -sf

todos:
	grep -r TODO carnival

docs:
	poetry run make -C docs html

dist:
	poetry publish
	git tag `poetry version -s`
	git push --tags
