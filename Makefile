help:
	@echo "make docker"
	@echo "         for linux"
	@echo "  "
	@echo "make docmac"
	@echo "         for Mac"


docker:
	/bin/bash sparse_checkout_shallow_clone.sh
	@cd ds/search_d3js_graph/;sudo service docker start;sudo su -c "docker build -t flask_test ." root; sudo su -c "docker run -it --rm  --publish 5000:5000 flask_test" root


install:
	sudo apt install -y libgraphviz-dev

pip:
	pip install -r requirements.txt

autopep8:
	find . -type f -name "*.py" -exec autopep8 --in-place --aggressive --aggressive "{}" \; 	
black:
	find . -type f -name "*.py" -exec black "{}" \; 

docmac:
	docker build -t pyast .
	docker run -it --rm pyast /bin/bash

