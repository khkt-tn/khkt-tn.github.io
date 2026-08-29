# Fish AI Research website

Public MkDocs presentation layer for the Fish AI research diary.

Scientific source: [khkt-tn/fish/research_diary](https://github.com/khkt-tn/fish/tree/main/research_diary)

The website repository does not replace or edit the scientific source. Journal
pages are synchronized from the source Markdown, while small referenced plots
are copied into the site with their provenance paths retained.

## Local setup

~~~bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/sync_research_diary.py
python scripts/build_journal_index.py
python scripts/validate_site.py
mkdocs serve
~~~

Or use:

~~~bash
./scripts/update_from_research.sh
./scripts/preview.sh
~~~

The update helper synchronizes, rebuilds the index, validates, and prints Git
status. It never commits or pushes.

## Build

~~~bash
mkdocs build --strict
~~~

GitHub Pages deployment uses the official GitHub Actions workflow in
.github/workflows/pages.yml.
