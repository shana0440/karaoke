.PHONY: clear
clear:
	-rm dataset/karaoke/karaoke*_out*.wav
	-rm dataset/songs/song*_out*.wav
	-rm dataset/zatsudan/zatsudan*_out*.wav

.PHONY: prepare
prepare:
	python prepare_karaoke.py

.PHONY: train
train:
	python train_cnn.py

.PHONY: predict
predict:
	python predict_karaoke.py
	python post_process.py