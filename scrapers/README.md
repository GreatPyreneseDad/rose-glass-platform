# Leelanau County Policies Scraper

Scrapes every document linked from the Leelanau County policies page and
consolidates them into a single Markdown file.

**Source page:** https://www.leelanau.gov/leelanau_county/county_policies.php
(53 documents at time of writing)

## Install

```bash
pip install -r requirements-scraper.txt
```

## Run

```bash
python leelanau_policies_scraper.py \
    --out leelanau_county_policies.md \
    --cache ./.policy_cache
```

The result is one Markdown file containing:

- A header with the source URL and compile date.
- A numbered table of contents linking to each document.
- One section per document with its source link, file type, and extracted text.

Downloaded source files are kept in `--cache` so re-runs are fast and you can
audit the originals.

## Options

| Flag | Default | Purpose |
|------|---------|---------|
| `--url` | the county policies page | Index page to scrape |
| `--out` | `leelanau_county_policies.md` | Output Markdown path |
| `--cache` | `./.policy_cache` | Where raw downloads are stored |
| `--delay` | `1.0` | Seconds between downloads (be polite) |
| `--limit` | `0` | Process only the first N docs (`0` = all) |
| `--expect` | `53` | Warn if the link count differs |

## How it works

1. Fetches the index page with a browser `User-Agent` (the county server
   returns **HTTP 403** to non-browser agents).
2. Extracts document links via `looks_like_document()` — matches `.pdf`,
   `.doc(x)`, spreadsheets, and common CMS download paths.
3. Downloads each file into the cache.
4. Extracts text: **PyMuPDF** for PDFs (fallback **pdfminer.six**),
   **python-docx** for `.docx`, plain read for `.txt`. Legacy `.doc` binaries
   are linked rather than parsed.
5. Writes the combined Markdown.

A failure on any single document is logged and the run continues; that document
still appears in the output with the error and a direct link.

## Notes / tuning

- If the found link count isn't 53, inspect the page HTML and adjust the
  `looks_like_document()` heuristic or the content-container selector in
  `extract_links()`.
- This environment's egress policy blocks `www.leelanau.gov`, so the script
  must be run somewhere with outbound access to that host.
- For scanned/image-only PDFs, text extraction yields nothing; add an OCR step
  (e.g. `pytesseract` over `fitz` page pixmaps) if needed.
