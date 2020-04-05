pypi:
	pip install --upgrade setuptools wheel twine
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -Rf build dist *.egg-info
