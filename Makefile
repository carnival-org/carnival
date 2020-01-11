.PHONY: dist

clean:
	rm -rf fabric_spt.egg-info dist

test:
	flake8 .
	mypy .
	pytest .


todos:
	grep -r TODO carnival

install:
	python3 setup.py install

dist:
	python3 setup.py sdist
	twine upload dist/*
	git tag `python3 -c "from carnival import __version__; print(__version__)"`
	git push --tags
