# CODEX SITE REPORT

## Repository

- Local path: `/home/diy-hus/khkt-tn.github.io`
- Remote: `https://github.com/khkt-tn/khkt-tn.github.io.git`
- Visibility: public
- Branch: `main`
- Launch commit SHA: `ceb2fe0df3556db6fb3e1ab8c6860cc902a3b38b`
- Launch commit message: `site: launch Fish AI research journal`
- Scientific source: `https://github.com/khkt-tn/fish/tree/main/research_diary`
- Scientific source commit recorded by sync: `36e24ed6a245086bc40bf502f29f298514521407`

## Website

- Pages URL: `https://khkt-tn.github.io/`
- Pages source: GitHub Actions (`build_type: workflow`)
- HTTPS enforced: yes
- Local strict build: PASS
- GitHub Actions build: PASS
- GitHub Actions deploy: PASS
- Public HTTP check: PASS (`HTTP/2 200`)
- Public homepage content check: PASS
- Public journal JSON check: PASS
- Workflow run: `https://github.com/khkt-tn/khkt-tn.github.io/actions/runs/33255003307`

## Content

- Journal entries: 16
- VERIFIED: 7
- PARTIAL: 3
- TO_VERIFY: 0
- PLANNED: 6
- Status source: YAML front matter synchronized from J01–J16
- Referenced small images copied: 8
- Result gallery images displayed: 6

## Media

- Video available: 0
- `TODO_UPLOAD` media rows represented as `Chờ video`: 12
- Raw TODO YouTube placeholders displayed to visitors: 0
- Media warnings: 14 journal pages reference media that is waiting for update
- TODO media is treated as a warning, not a validation failure

## Validation

- Markdown synchronization: PASS (21 mapped Markdown files)
- J01–J16 presence: PASS
- YAML parsing and required metadata: PASS
- Status values and duplicate journal IDs: PASS
- Local Markdown/HTML links and image paths: PASS
- Source Markdown hash check: PASS
- Scientific source diff check: PASS
- Future completed-entry cutoff check: PASS
- Secret-pattern scan: PASS
- Unexpected file larger than 5 MiB: PASS
- MkDocs `build --strict`: PASS
- Local route preview: PASS for homepage, project, journal index, J01, J16, experiments, timeline, results, media, evidence, contributions, and journal JSON
- Responsive CSS audit: PASS for the intended 375 px, 768 px, 1024 px, and 1440 px layouts
- Browser screenshot audit: not run because no headless browser executable was available locally
- JavaScript: vanilla JS only; no analytics, tracking, cookies, ads, or autoplay
- Build note: MkDocs Material emitted its informational notice about the future MkDocs 2.0 project; it did not produce a strict-build failure

## Files created

- MkDocs configuration, pinned Python requirements, README, `.gitignore`, and `.nojekyll`
- GitHub Pages workflow at `.github/workflows/pages.yml`
- Landing, project, journal, experiment, timeline, result, media, evidence, and contribution pages under `docs/`
- J01–J16 synchronized journal pages with preserved YAML front matter
- Responsive research UI in `docs/assets/css/extra.css`
- Vanilla JS enhancements in `docs/assets/js/extra.js`
- Generated journal and synchronization JSON under `docs/assets/data/`
- Eight source-referenced plots under `docs/assets/images/research/`
- Sync, index, validation, update, and preview helpers under `scripts/`

## Remaining manual actions

- None required for the current public deployment.
- For future media updates, replace the 12 YouTube placeholders in the scientific Markdown source, then run:

  ~~~bash
  cd /home/diy-hus/khkt-tn.github.io
  source .venv/bin/activate
  ./scripts/update_from_research.sh
  ~~~

  Review the resulting Git diff before committing and pushing.

## Source preservation

No file in `/home/diy-hus/fish/research_diary` was modified by the website pipeline. Raw data, models, outputs, notebooks, scientific metrics, and prior research results were not edited or staged. The unrelated pre-existing dirty files in the `fish` worktree were preserved.
