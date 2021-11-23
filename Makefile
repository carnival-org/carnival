.PHONY: all
all: test_deps qa docs test

.PHONY: clean
clean: nodev
	rm -rf carnival.egg-info dist build __pycache__ .mypy_cache .pytest_cache .coverage

.PHONY: test_deps
test_deps:
	poetry install --no-root

.PHONY: qa
qa:
	poetry run flake8 .
	poetry run mypy .

.PHONY: test
test: docs qa dev
	poetry run python3 -m pytest -x --cov-report term --cov=carnival -vv tests/

.PHONY: test_fast
test_fast: dev
	poetry run python3 -m pytest -x --cov-report term --cov=carnival -vv -m "not slow" tests/

.PHONY: test_local
test_local: dev
	poetry run python3 -m pytest -x --cov-report term --cov=carnival -vv -m "not remote" tests/

.PHONY: dev
dev:
	docker-compose -f testdata/docker-compose.yml up --build -d --remove-orphans

.PHONY: nodev
nodev:
	docker-compose -f testdata/docker-compose.yml rm -sf
	ssh-keygen -R [127.0.0.1]:22222
	ssh-keygen -R [127.0.0.1]:22223

.PHONY: todos
todos:
	grep -r TODO carnival

.PHONY: docs
docs:
	poetry run make -C docs html

.PHONY: dist
dist:
	poetry publish --build
	git tag `poetry version -s`
	git push --tags
