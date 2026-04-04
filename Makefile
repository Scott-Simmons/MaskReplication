SERVER_PORT ?= 9437

all: clean build

clean:
	@echo removing build dir
	rm -rf build/

build:
	@echo generating blog
	python -m blog.generate

serve:
	@echo serving on $(SERVER_PORT)
	python -m http.server $(SERVER_PORT) --directory build

.PHONY: FORCE
FORCE:

.PHONY: clean serve
