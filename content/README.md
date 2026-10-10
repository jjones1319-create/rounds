# content/

Source of truth for MCAT content. `tools/validate.py` checks it and `build.py` bundles it into `data/mcat.json`,
which the app fetches at runtime. A validation error stops the build.

- `mcat/M1.json`, `mcat/M2.json`, …: question blocks (schema: `docs/MCAT_SPEC.md` §8).
- `mcat/guides/<section>.json`: "What's tested" guides (schema: `docs/MCAT_GUIDES_SPEC.md` §4), one per section:
  `chem_phys`, `cars`, `bio_biochem`, `psych_soc`.

Board questions still live in `questions/*.py` and are bundled into `data/boards.json`; they may move here later.
Run `py tools/validate.py` to validate without building; the coverage report goes to `work/mcat_coverage.md`.
