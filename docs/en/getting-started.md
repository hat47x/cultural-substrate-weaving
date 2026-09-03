# Getting started

This repository serves both people who use the method and people who maintain and release it.

## Runtime environment

The method can be used with supplied material alone. Web search / browsing is useful when the task requires current fact checking, external context, or source discovery. If Web search is unavailable, do not fill missing facts by guesswork; preserve them as missing material or further search targets. See each platform guide for how to enable browsing when you need it.

## People who use the method

Download the ZIP for your platform and locale from GitHub Releases. You do not need to edit the repository.

The current Microsoft 365 Copilot distribution is a limited adapter: only the content under `instructions.txt` is treated as agent instructions. If you need reliable execution of the full method, review the [Microsoft 365 Copilot guide](platforms/microsoft-copilot.md) before choosing that environment.

## People who maintain and release the method

Clone the repository, edit `src/ja-JP/` or a translation under `src/<locale>/`, and run `make check`. Platform-specific files are generated.

## Choosing a platform

- Broad use in a subscription chat: a ChatGPT custom GPT.
- Coding and repository analysis: Codex or Claude Code.
- Documents and SharePoint inside Microsoft 365: a Microsoft 365 Copilot agent, with the current limited-adapter boundary described in the platform guide.
- One canonical method across several AI systems: maintain this repository and generate adapters.
