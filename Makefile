.PHONY: generate-blog-post serve run-evals run-analysis

generate-blog-post:
	python -m blog.generate

serve: generate-blog-post
	python -m http.server 9437 --directory output

run-evals:
	@echo "TODO: run evals"

run-analysis:
	@echo "TODO: run analysis"
