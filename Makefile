.PHONY: setup
setup:
	conda env create --file=environment.yml --name=karaoke

.PHONY: activate
activate:
	# conda activate karaoke # this not going to work, just remine me need to run this
