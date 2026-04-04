.PHONY: blog-post serve run-analysis

clean:
	rm -rf build/

build:
	python -m blog.generate

serve: blog-post
	python -m http.server 9437 --directory output

.PHONY: FORCE
FORCE:

