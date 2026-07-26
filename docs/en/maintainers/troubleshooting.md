# Troubleshooting

## A translation is reported as stale

The canonical Japanese file hash changed. Update the corresponding translation, review it, then run `scripts/update_translation_hashes.py`.

## Codex does not show the skill

Check the extraction folder, frontmatter, selected locale package, and restart Codex.

## Claude Marketplace cannot find a plugin

Confirm `OWNER/REPO`, the default branch, and `.claude-plugin/marketplace.json`.

## A GPT does not use Knowledge

Keep behavioral rules in Instructions and detailed references in Knowledge. Verify that the localized Instructions refer to the Knowledge files.

## Microsoft agent validation fails

Check `atk doctor`, environment values, GUIDs, URLs, icons, and the manifest schema. Use the project under the selected locale.
