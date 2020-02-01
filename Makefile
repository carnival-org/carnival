.PHONY: dist

clean:
	rm -rf fabric_spt.egg-info dist

test_deps:
	pip3 install -qr requirements_dev.txt
	pip3 install -qe .

test:
	flake8 .
	mypy --warn-unused-ignores --package carnival
	pytest --cov-fail-under=58 --cov-report term --cov=carnival tests/

todos:
	grep -r TODO carnival

install:
	python3 setup.py install

dist:
	python3 setup.py sdist
	twine upload dist/*
	git tag `python3 -c "print(open('VERSION').read().strip())"`
	git push --tags
