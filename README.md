# Connected Systems BDD — API to UI Journey

I built this to demonstrate how a test framework can bridge two separate systems, an API backend and a web UI where the data flows dynamically from one into the other. No hardcoded values, no shortcuts.

---

## What This Tests

A supply chain journey where I create a pet via the Petstore API and use that pet's data to drive a checkout flow on SauceDemo. The UI never knows the data in advance, it comes entirely from the API response at runtime.

---

## Tech Stack

| Tool         | Purpose                 |
| ------------ | ----------------------- |
| Python 3.11+ | Language                |
| Behave       | BDD framework (Gherkin) |
| Playwright   | Browser automation      |
| Requests     | API calls               |

---

## Getting Started

### Clone and enter project

```bash
git clone https://github.com/UmarRiaz00095/connected-system.git
cd connected_system
```

### Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
python -m playwright install
```

---

## Running the Tests

```bash
# Run everything
behave

# Smoke tests only
behave --tags=smoke

# Full regression suite
behave --tags=regression

# Watch it run in the browser
HEADLESS=false behave
```

---

## HTML Report

I added a lightweight HTML report using `behave-html-formatter` , no Java or external tools needed.

### Generate the Report

```bash
behave -f behave_html_formatter:HTMLFormatter -o reports/report.html
```

### Open the Report

```bash
# Windows
start reports/report.html

# Mac
open reports/report.html
```

---

## Why I Built It This Way

### config.py as single source of truth

I didn't want URLs, timeouts, or retry counts scattered across files. Everything lives in `config.py`, one change and it propagates everywhere.

### Credentials in .env

For this demo the credentials are hardcoded in `config.py` with a clear comment explaining they shouldn't be in production code.

In a real project:

* Use `python-dotenv`
* Store secrets in a `.env` file
* Add `.env` to `.gitignore`
* Use GitHub Actions secrets in CI

### Retry logic in the API client

The Petstore API is a public demo — it's flaky by nature. Instead of failing immediately, I retry 3 times with a short delay before giving up.

---

## CI/CD

In a pipeline:

* Run **smoke tests** on every commit
* Run **regression suite** nightly

---

## Notes

* Screenshots on failure are saved to `screenshots/`
* Petstore is a public API, occasional timeouts are expected and handled
* SauceDemo credentials are intentionally public for testing purposes
* Set `BROWSER_HEADLESS = True` in `config.py` for CI runs
