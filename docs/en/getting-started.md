# Getting started

This repository serves two audiences.

The method assumes it can pull in current facts and context via dynamic web search. Enable web search / browsing on whichever platform you use; see each platform guide for how.

## People who use the method

Download the ZIP for your platform and locale from GitHub Releases. You do not need to edit the repository.

## People who maintain and release the method

Clone the repository, edit `src/ja-JP/` or a translation under `src/<locale>/`, and run `make check`. Platform-specific files are generated.

## Choosing a platform

- Broad use in a subscription chat: a ChatGPT custom GPT.
- Coding and repository analysis: Codex or Claude Code.
- Documents and SharePoint inside Microsoft 365: a Microsoft 365 Copilot agent.
- One canonical method across several AI systems: maintain this repository and generate adapters.
