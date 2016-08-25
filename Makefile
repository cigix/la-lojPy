python_files=	\
	base.py	\
	test.py	\
	words.py

test:
	./test.py
	pylint $(python_files)
