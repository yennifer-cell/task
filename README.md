# Inventory Management System (Flask)

Simple Flask REST API to manage inventory items with an external OpenFoodFacts lookup and a CLI client.

Quick start

1. Create venv and install:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the API:

```bash
python app.py
```

3. Use the CLI in another terminal (examples):

```bash
python cli.py list
python cli.py add "New Product" --price 2.5 --stock 10
python cli.py fetch Almond
```

Run tests:

```bash
pytest -q
```
# task
