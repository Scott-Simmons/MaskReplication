SERVER_PORT ?= 9437

all: clean build

clean:
	@echo removing build dir
	rm -rf build/

build:
	@echo generating blog
	python -m blog.generate

review:
	@echo reviewing sections
	python -m blog.review

serve:
	@echo serving on $(SERVER_PORT)
	python -m http.server $(SERVER_PORT) --directory build

release: build
	@VERSION=$$(python -c "from blog.version import VERSION; print(VERSION)"); \
	if [ -d "versions/$$VERSION" ]; then \
		echo "ERROR: versions/$$VERSION already exists. Bump VERSION first."; \
		exit 1; \
	fi; \
	mkdir -p versions/$$VERSION; \
	rsync -a --exclude='versions' build/ versions/$$VERSION/; \
	echo "Archived version $$VERSION to versions/$$VERSION/"

.PHONY: FORCE
FORCE:

.PHONY: clean serve review release
