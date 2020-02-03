.PHONY: dist

clean:
	rm -rf fabric_spt.egg-info dist

test_deps:
	pip3 install -qr requirements_dev.txt
	pip3 install -qe .

qa:
	flake8 .
	mypy --warn-unused-ignores --package carnival

test: qa
	pytest -x --cov-fail-under=60 --cov-report term --cov=carnival tests/

dev:
	docker-compose up --build -d --remove-orphans --force-recreate

nodev:
	docker-compose rm -sf

todos:
	grep -r TODO carnival

install:
	python3 setup.py install

dist:
	python3 setup.py sdist
	twine upload dist/*
	git tag `python3 -c "print(open('VERSION').read().strip())"`
	git push --tags
