# Training Advisor
Search-driven training recommender for customer service reps, built from the Alkami training catalog.

Quick start: `python scripts/build.py`, then open `dist/training-advisor.html`.
See `CLAUDE.md` for architecture, rules, brand notes, and workflow.

To update after the catalog changes: replace `data/training_catalog.xlsx`, then run
`python scripts/build_catalog.py && python scripts/build.py`.
