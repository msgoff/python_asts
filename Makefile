help:
	@echo "make docker"
	@echo "         for linux"
	@echo "  "
	@echo "make docmac"
	@echo "         for Mac"


docker:
	sudo service docker start
	sudo docker build  -t pyast .
	sudo docker run -it --rm pyast /bin/bash

docmac:
	docker build -t pyast .
	docker run -it --rm pyast /bin/bash

