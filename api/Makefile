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

.PHONY: backup-model
backup-model:
	# backup dataset/models/karaoke_model
	@echo "Backing up model..."
	@timestamp=$$(date +%Y%m%d%H%M%S); \
	cp -r dataset/models/karaoke_model dataset/models/karaoke_model.$$timestamp.bak
