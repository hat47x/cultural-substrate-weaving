# Repository instructions

The canonical method is under `src/ja-JP/`; `src/en-US/` is a structurally parallel translation.

For repository maintenance:
- edit canonical or translated source deliberately;
- keep identical relative file structures across locales;
- update translation hashes after translation review;
- regenerate adapters with `make build`;
- run `make check`;
- never hand-edit `dist/`.
