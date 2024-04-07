style:
	python3 -m isort .
	python3 -m black .

check:
	python3 -m isort --check .
	python3 -m black --check .
	python3 -m flake8 --ignore=E501 ./*.py

status:
	./status.sh

deploy:
	./deploy_services.sh
