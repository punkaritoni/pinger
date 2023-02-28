VENV := venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install --upgrade pip setuptools setuptools_scm wheel build
	./$(VENV)/bin/pip install -r requirements.txt
	./$(VENV)/bin/pip install -e .

venv: $(VENV)/bin/activate

test: venv
	./$(VENV)/bin/pylint library

run: venv
	./$(VENV)/bin/python3 library/pinger/main.py

clean:
	rm -rf $(VENV)