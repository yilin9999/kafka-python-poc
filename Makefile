#!make

# make headline colorful
TAG="\n\n\033[0;32m\#\#\# "
END=" \#\#\# \033[0m\n"

venv:
	@echo $(TAG)Generate python 3.7.4 virtualenv$(END)
	pip3 install virtualenv==16.7.9 --user
	pyenv local 3.7.4
	virtualenv --python=python --no-site-packages venv
	venv/bin/pip install --upgrade pip setuptools wheel
	venv/bin/pip install -r requirements.txt

run:
	sh -c ' . venv/bin/activate ; python3 kafka-producer-consumer-poc.py'

lint:
	@echo $(TAG)Running Lint$(END)
	sh -c ' . venv/bin/activate ; flake8 *.py --count --ignore=E501,E126'
