init:
	pip install -r requirements.txt
	
docs:
	pip install sphinx sphinx_bootstrap_theme
	rm -rf ./docs/source/
	sphinx-apidoc -o ./docs/source/ ./pytwask
	cd ./docs/ && $(MAKE) html
	
docs_clean:
	cd ./docs/ && $(MAKE) clean

.PHONY: init docs docs_clean