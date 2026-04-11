SERVER_PORT ?= 9437
PYTHON := uv run python
SCOUT  := uv run scout

all: build

clean:
	@echo removing build and scan dirs
	rm -rf build/ scan_logs/

build: clean scan
	@echo generating blog
	$(PYTHON) -m blog.generate

scan:
	@echo running error scanner
	$(SCOUT) scan blog/error_scanner.py \
		-T eval_logs/ \
		-F "score.honesty = 'error' or score.honesty IS NULL" \
		--scans scan_logs/
	@echo aggregating results
	$(PYTHON) -m blog.aggregate_scan

review:
	@echo reviewing sections
	$(PYTHON) -m blog.review

serve:
	@echo serving on $(SERVER_PORT)
	$(PYTHON) -m http.server $(SERVER_PORT) --directory build

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
