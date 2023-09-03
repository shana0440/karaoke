.PHONY: dev
dev:
	uvicorn app:app --host 0.0.0.0 --port=8888 --reload

.PHONY: migrate
migrate:
	alembic upgrade head 