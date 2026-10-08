# Hospital Emergency Queue

A Python-only Hospital Emergency Queue webpage.

## Features

- Priority Queue
- Critical patients served first
- Add patient
- Treat next patient
- Load demo patients
- Clear queue
- Statistics
- No JavaScript
- No Flask
- No external Python packages

## Run locally

```bash
python app.py
```

Then open `http://127.0.0.1:5000`.

## Deploy on Vercel

This repository includes:

- `vercel.json`
- `api/index.py`

Vercel uses `api/index.py` as the Python serverless function.

Open the deployed Vercel URL to use the webpage.

> Note: the queue is stored in memory, so it is suitable for a college/demo project. Serverless instances are not a persistent database.
