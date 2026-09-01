.PHONY: build validate test tokens package release-validate check release-check clean update-en-hashes living-lab-check living-lab-summary japanese-docs-check

build:
	python scripts/build.py

validate:
	python scripts/validate.py

japanese-docs-check:
	python scripts/check_natural_japanese_review.py

test:
	python -m unittest discover -s tests

tokens:
	python scripts/token_budget.py

package:
	python scripts/package.py

release-validate:
	python scripts/validate_release.py

living-lab-check:
	python scripts/validate_living_lab.py

living-lab-summary:
	python scripts/summarize_living_lab.py

check: build validate japanese-docs-check test tokens living-lab-check living-lab-summary

release-check: check package release-validate

clean:
	rm -rf dist .tmp

update-en-hashes:
	python scripts/update_translation_hashes.py --locale en-US
