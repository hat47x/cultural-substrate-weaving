.PHONY: build validate test tokens package check release-check clean update-en-hashes living-lab-check living-lab-summary

build:
	python scripts/build.py

validate:
	python scripts/validate.py

test:
	python -m unittest discover -s tests

tokens:
	python scripts/token_budget.py

package:
	python scripts/package.py

living-lab-check:
	python scripts/validate_living_lab.py

living-lab-summary:
	python scripts/summarize_living_lab.py

check: build validate test tokens living-lab-check living-lab-summary

release-check: check package

clean:
	rm -rf dist .tmp

update-en-hashes:
	python scripts/update_translation_hashes.py --locale en-US
