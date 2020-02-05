.PHONY: dist clean qa test dev nodev todos install

clean:
	rm -rf fabric_spt.egg-info dist

test_deps:
	pip3 install -qr requirements_dev.txt
	pip3 install -qe .

qa:
	flake8 .
	mypy --warn-unused-ignores --package carnival

test: qa
	pytest -x --cov-fail-under=90 --cov-report term --cov=carnival tests/

dev:
	docker-compose -f tests/docker-compose.yml up --build -d --remove-orphans --force-recreate

nodev:
	docker-compose -f tests/docker-compose.yml rm -sf

todos:
	grep -r TODO carnival

install:
	python3 setup.py install

dist:
	python3 setup.py sdist
	twine upload dist/*
	git tag `cat setup.py | grep VERSION | grep -v version | cut -d= -f2 | tr -d "[:space:]"`
	git push --tags
