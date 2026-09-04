.PHONY: build generated-artifacts-check validate test tokens package release-validate check release-check release-tag-contract release-remote-tag-contract clean update-en-hashes living-lab-check living-lab-summary japanese-docs-check repository-contracts main-contract

.NOTPARALLEL: check release-check

repository-contracts:
	python scripts/check_branch_version.py --ref "$$(git branch --show-current)"

main-contract:
	@branch="$$(git branch --show-current)"; \
	if [ "$$branch" != "main" ]; then \
		echo "main-contract must be run on the main branch (current: $$branch)" >&2; \
		exit 1; \
	fi
	python scripts/check_main_push_contract.py --parents "$$(git show -s --format=%P HEAD)"

build:
	python scripts/build.py

generated-artifacts-check: build
	python scripts/check_generated_artifacts.py

validate:
	python scripts/validate.py
	python scripts/validate_m365_profile.py

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
	python scripts/validate_living_lab.py --record-set research/living-lab/observations/*.json

living-lab-summary:
	python scripts/summarize_living_lab.py

check: repository-contracts generated-artifacts-check validate japanese-docs-check test tokens living-lab-check living-lab-summary

release-check: check package release-validate

release-tag-contract: release-validate
	python scripts/check_release_tag.py --tag "$(TAG)"

release-remote-tag-contract:
	python scripts/check_remote_release_tag.py --tag "$(TAG)"

clean:
	rm -rf dist .tmp

update-en-hashes:
	python scripts/update_translation_hashes.py --locale en-US
