.PHONY: environment
environment:
	pyenv install -s 3.10.0
	pyenv uninstall --force user-manager
	pyenv virtualenv 3.10.0 --force user-manager
	pyenv local user-manager

.PHONY: install
install:
	pip freeze | xargs -r pip uninstall -y && \
	pip install -r requirements-dev.txt && \
	pre-commit install

.PHONY: db_init
db_init:
	docker-compose up -d database

.PHONY: db_generate_migration
db_generate_migration: db_run_migrations
	PYTHONPATH=. \
	alembic revision --autogenerate -m "$(description)"

.PHONY: db_run_migrations
db_run_migrations: db_init
	PYTHONPATH=. \
	alembic upgrade head

.PHONY: cache_init
cache_init:
	docker-compose up -d cache

.PHONY: broker_init
broker_init:
	docker-compose up -d broker \
	|| echo "Could not start broker"

.PHONY: test
test:
	docker-compose down && \
	PYTHONPATH=. \
	python -m pytest --cov=app -s

.PHONY: run
run: db_run_migrations cache_init broker_init
	uvicorn --reload --port=8001 app.run:api
