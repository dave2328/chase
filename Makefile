pypi:
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*
	rm -Rf build dist *.egg-info
