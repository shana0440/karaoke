.PHONY: dev
dev:
	uvicorn app:app --host 0.0.0.0 --port=8888 --reload

.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: prepare
prepare:
	python train_model.py --prepare

.PHONY: train
train:
	python train_model.py --train

.PHONY: prepare-train
prepare-train:
	python train_model.py

.PHONY: backup-model
backup-model:
	# backup dataset/models/karaoke_model
	@echo "Backing up model..."
	@timestamp=$$(date +%Y%m%d%H%M%S); \
	cp -r dataset/models/karaoke_model dataset/models/karaoke_model.$$timestamp.bak


.PHONY: clear
clear:
	rm dataset/zatsudan/*_out_*.wav
	rm dataset/songs/*_out_*.wav