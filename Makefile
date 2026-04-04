.PHONY: blog-post serve run-analysis

blog-post:
	python -m blog.generate

serve: blog-post
	python -m http.server 9437 --directory output

