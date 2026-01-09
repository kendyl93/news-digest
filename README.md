# Daily News Digest (PL)

A Python-based tool that collects articles from Polish news RSS feeds, filters out clickbait and low-quality content, ranks what actually matters, and generates a short daily digest (Markdown + optional tweet-sized summary).

The goal is to answer one question:
**“What happened today that is worth my time?”**

---

## Requirements

- Python **3.10+**
- Git
- Internet connection (RSS feeds)

## Setup (First Time)

### 1. Clone the repository

```bash
git clone <REPO_URL>
cd news-digest
```

2. Create a virtual environment

```
python3 -m venv .venv
```

3. Activate the virtual environment

macOS / Linux

```
source .venv/bin/activate
```

Windows (PowerShell)

```
.venv\Scripts\Activate.ps1
```

You should now see (.venv) in your terminal prompt.

4. Install Dependencies
   Install from requirements.txt

```
pip install -r requirements.txt
```

5. Verify installation:

Running the Application
With the virtual environment activated:

```
python main.py
```

This will:

fetch RSS articles

filter and rank them

generate a daily digest file in outputs/

6. Freezing Dependencies (Updating requirements.txt). If you add or update dependencies:

```
pip freeze > requirements.txt
```
