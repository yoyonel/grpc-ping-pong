wheel:
	@echo "Building python project..."
	@python setup.py bdist_wheel

sdist:
	@echo "Building python project..."
	@python setup.py sdist
