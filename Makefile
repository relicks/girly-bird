.PHONY = all init install run

all: init install run

init:
	python3 -m venv .venv
	./.venv/bin/python3 -m pip install --upgrade pip

install:
	./.venv/bin/pip install .

run:
	./.venv/bin/python3 ./main.py
