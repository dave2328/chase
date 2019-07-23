pypi:
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	twine upload dist/*
	rm -Rf build dist *.egg-info
