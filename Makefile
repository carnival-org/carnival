clean:
	rm -rf fabric_spt.egg-info

test:
	flake8 .
	mypy .
	pytest .
