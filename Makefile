SERVER_PORT ?= 9437
PYTHON := uv run python
SCOUT  := uv run scout

all: build

clean:
	@echo removing build, scan, and decrypted eval dirs
	rm -rf build/ scan_logs/ eval_logs_dec/

build: clean scan
	@echo generating blog
	$(PYTHON) -m blog.generate

decrypt:
	@echo decrypting eval logs
	$(PYTHON) -m blog.crypto decrypt eval_logs/ eval_logs_dec/

scan: decrypt
	@echo running error scanner
	$(SCOUT) scan blog/error_scanner.py \
		-T eval_logs_dec/ \
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

# Generate a new key pair (run once; keep age_private.key secret)
keygen:
	$(PYTHON) -m blog.crypto keygen

# Encrypt a single eval log and place it in eval_logs/
# Usage: make encrypt-log LOG=path/to/file.eval
encrypt-log:
	@test -n "$(LOG)" || (echo "Usage: make encrypt-log LOG=path/to/file.eval"; exit 1)
	$(PYTHON) -m blog.crypto encrypt $(LOG) eval_logs/$(notdir $(LOG)).enc
	@echo "Done. git add eval_logs/$(notdir $(LOG)).enc"

release: build
	@VERSION=$$($(PYTHON) -c "from blog.version import VERSION; print(VERSION)"); \
	if [ -d "versions/$$VERSION" ]; then \
		echo "ERROR: versions/$$VERSION already exists. Bump VERSION first."; \
		exit 1; \
	fi; \
	mkdir -p versions/$$VERSION; \
	rsync -a --exclude='versions' build/ versions/$$VERSION/; \
	echo "Archived version $$VERSION to versions/$$VERSION/"

.PHONY: FORCE
FORCE:

.PHONY: clean serve review release decrypt keygen encrypt-log
