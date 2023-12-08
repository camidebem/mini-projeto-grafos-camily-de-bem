VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

# default arguments
nodes = "fb-pages-food.nodes"
edges = "fb-pages-food.edges"

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run: $(VENV)/bin/activate
	$(PYTHON) analise-comunidades.py $(nodes) $(edges)

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
