# Inventory Management System — End-to-end walkthrough

---

## Title

- **Project:** Inventory Management System (Flask)
- **Audience:** Instructor / teammates / demo
---

## Slide 1 — Problem Statement

- Need: Administrator portal for a small retail company to manage inventory.
- Requirements: CRUD endpoints, external product lookup (OpenFoodFacts), CLI frontend, unit tests, README and Git history.
- Presenter notes: Emphasize business pain: reduce manual inventory errors and enrich product data.

---

## Slide 2 — High-level Design

- Components:
  - Flask REST API (endpoints for inventory)
  - In-memory mock database (list/array)
  - External fetch helper (OpenFoodFacts)
  - CLI client to call API
  - Tests (pytest + mocks)
- Presenter notes: Show a simple diagram (API <-> DB, API <-> OpenFoodFacts, CLI <-> API).

---

## Slide 3 — API Routes (Design)

- GET /inventory → list all items
- GET /inventory/<id> → get item
- POST /inventory → add item
- PATCH /inventory/<id> → update item
- DELETE /inventory/<id> → remove item
- GET /fetch?q=... → external lookup by barcode or name
- Presenter notes: Explain inputs/outputs and HTTP status codes used (200, 201, 404, 400).

---

## Slide 4 — Data Model (Mock DB)

- Example item fields:
  - id, name, brand, price, stock, barcode
- Data stored in `inventory_db` list in `inventory.py`.
- Presenter notes: Explain why mock DB was used (simplicity for lab), and how it can be swapped for persistent storage.

---

## Slide 5 — External API Integration

- Use OpenFoodFacts endpoints:
  - Product by barcode: `https://world.openfoodfacts.org/api/v0/product/{barcode}.json`
  - Search by name: `https://world.openfoodfacts.org/cgi/search.pl?search_terms=...&json=1`
- Implemented in `fetch_external_product(q)` in `inventory.py`.
- Presenter notes: Mention error handling and mocking for tests to avoid network dependency.

---

## Slide 6 — CLI Frontend

- `cli.py` supports commands:
  - `list`, `get <id>`, `add`, `update`, `delete`, `fetch <q>`
- Demonstrates usage examples and how the CLI maps to API endpoints.
- Presenter notes: Show example commands and one live demo plan.

---

## Slide 7 — Testing Strategy

- Tests in `tests/test_api.py` using `pytest` and `unittest.mock`:
  - Test CRUD flow (create → get → patch → delete)
  - Mock `requests.get` for external API fetch tests
- Presenter notes: Explain why mocking is important and show test run output (4 passed).

---

## Slide 8 — Project Files Overview

- `app.py` — Flask app and endpoints
- `inventory.py` — in-memory DB and external API helper
- `cli.py` — command-line client
- `tests/test_api.py` — pytest suite
- `requirements.txt`, `README.md`, `.gitignore`
- Presenter notes: Point attendees to the repository root and key files.

---

## Slide 9 — Demo Plan (Live)

1. Start Flask app: `python app.py`
2. In another terminal: `python cli.py list` → show initial items
3. Add an item: `python cli.py add "Demo Item" --price 2.5 --stock 10`
4. Fetch external: `python cli.py fetch Almond` (show mocked behavior during test)
5. Run tests: `pytest -q`
- Presenter notes: Keep each step short and show expected output.

---

## Slide 10 — Git & Submission

- Local git repo initialized and committed.
- Recommended: push to GitHub, create feature branches, open PRs to demonstrate Git workflow.
- Presenter notes: Walk through the commands to push and create a branch.

---

## Slide 11 — Next Steps / Enhancements

- Replace in-memory DB with SQLite or PostgreSQL
- Add authentication and admin UI (Flask or a lightweight frontend)
- Add CI (GitHub Actions) to run tests on PRs
- Add pagination, filtering, and CSV import/export
- Presenter notes: Choose 2-3 realistic next steps to propose.

---

## Slide 12 — Q&A / Contact

- Recap the main deliverables and where code lives.
- Provide contact / GitHub repo link (if available).
- Presenter notes: Invite questions and offer to walk through code paths live.
