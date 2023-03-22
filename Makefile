black:
	black --line-length 79 ./chalicelib/*.py

lint:
	pylint ./chalicelib/ --disable=import-error,line-too-long,too-many-arguments,too-few-public-methods,missing-module-docstring,protected-access,R0801,C0103,R1720

test:
	pytest tests/*.py