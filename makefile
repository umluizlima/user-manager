.PHONY: install
install:
	pip install -r requirements-dev.txt && \
	pre-commit install

.PHONY: db_init
db_init:
	docker-compose up -d database

.PHONY: test
test:
	docker-compose down && \
	PYTHONPATH=. \
	python -m pytest --cov=app -s

.PHONY: run
run: db_init
	uvicorn --reload app.api:api
