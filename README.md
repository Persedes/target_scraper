# target_scraper
Scrape price for a target item and notify about changes

# Installation

Make sure you have [poetry](https://python-poetry.org/) and python(>=3.6.1) installed.

```bash 
poetry install
```

Next create a .env file (or set the environmentvariables manually) for the following vars:

```
APP_PASSWORD=SMTPPASSWORD
SENDER=EMAIL_SENDER
TO=EMAIL_1, EMAIL_2, EMAIL_3, etc
```

# Usage

```bash 
# when using poetry 
poetry run python scrape_stroller.py
```
