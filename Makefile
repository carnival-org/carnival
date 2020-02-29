.PHONY: dist clean qa test dev nodev todos install docs test_deps

clean:
	rm -rf carnival.egg-info dist build

test_deps:
	pip3 install -qr requirements_dev.txt
	python setup.py develop

qa:
	flake8 .
	mypy --warn-unused-ignores --package carnival

test: qa docs test_deps
	pytest -x --cov-report term --cov=carnival -vv tests/

test_fast: qa
	pytest -x --cov-report term --cov=carnival -vv -m "not slow" tests/

dev:
	docker-compose -f testdata/docker-compose.yml up --build -d --remove-orphans --force-recreate

nodev:
	docker-compose -f testdata/docker-compose.yml rm -sf

todos:
	grep -r TODO carnival

install:
	pip3 install --force-reinstall .

docs:
	pip install sphinx
	make -C docs html

dist:
	python3 setup.py sdist
	twine upload dist/*
	git tag `cat setup.py | grep VERSION | grep -v version | cut -d= -f2 | tr -d "[:space:]"`
	git push --tags
