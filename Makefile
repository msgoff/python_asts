help:
	@echo "make docker"
	@echo "         for linux"
	@echo "  "
	@echo "make docmac"
	@echo "         for Mac"


docker:
	@cd ds/search_d3js_graph/;sudo service docker start;sudo su -c "docker build -t flask_test ." root; sudo su -c "docker run -it --rm  --publish 5000:5000 flask_test" root
docmac:
	docker build -t pyast .
	docker run -it --rm pyast /bin/bash

