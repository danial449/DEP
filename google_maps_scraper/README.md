# Google Maps Scraper

This is simple scraper that uses Playwright to extract data from Google Maps.

## To Install:

- (Optional: create & activate a virtual environment) `virtualenv venv`, then `env/Scripts/activate` (in Window)

- `pip install -r requirements.txt`
- `playwright install chromium`

## to Run:

### A single search:

- `python3 main.py -s "<what & where to search for>" -t <how many>`

### Multiple searches at once

1. Add searches in `input.txt`, each search should be in a new line as shown in the example (check `input.txt`)
2. Then run: `python3 main.py`
3. If you pass `-t=<how many>` it will be applied to all the searches.
