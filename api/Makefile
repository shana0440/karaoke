.PHONY: dev
dev:
	uvicorn app:app --host 0.0.0.0 --port=8888 --reload

.PHONY: migrate
migrate:
	alembic upgrade head 

.PHONY: prepare
prepare:
	python prepare_dataset.py

.PHONY: train
train:
	python train_cnn.py