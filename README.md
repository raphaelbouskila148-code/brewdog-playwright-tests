# BrewDog USA – UI Test Automation

![Playwright Tests](https://github.com/raphaelbouskila148-code/brewdog-playwright-tests/actions/workflows/playwright.yml/badge.svg)

Automated UI tests for the [BrewDog USA](https://usa.brewdog.com) e-commerce site, written in **Python** with **Playwright** and **pytest**, and run automatically on every change with **GitHub Actions**.

This project continues my manual testing of the same site: I executed 246 test cases and reported 72 bugs in the [BrewDog STR report](https://raphaelbouskila148-code.github.io/raphael-QA-HTML1/brewdog-str.pdf). Here I automated the highest-value flows from that test plan so they can be re-run in minutes on every browser.

**📊 [Latest test report](https://raphaelbouskila148-code.github.io/brewdog-playwright-tests/)**

---

## What is tested

26 automated tests, run on 3 browser engines (Chromium, Firefox, WebKit) plus an emulated iPhone.

| Area | Tests | What is checked |
|---|---|---|
| Homepage & age gate | 4 | Page loads, age gate is shown to new visitors, "Confirm" closes it and is remembered |
| Shop categories | 7 | Beer, IPAs, Lagers, Variety Packs, Non-Alcoholics, Merch each list products; clicking a product opens it |
| Product page | 3 | Name, price in USD and "Add to cart" button are shown |
| Search | 3 | Results for "IPA"; clear message for no matches, with no unfilled template text |
| Cart | 3 | New cart is empty; adding a product updates the cart and the cart page |
| Footer | 4 | Shipping, Contact, Terms and Privacy links point to the right pages |
| Mobile | 2 | Homepage and category pages fit an iPhone screen with no sideways scrolling |

Tests are tagged so you can run just a group: `smoke` (quick health check), `regression` (deeper flows), `mobile`.

> The tests never go to checkout or place an order.

## Tech stack

- **Python 3.13**, **Playwright**, **pytest**
- **Page Object Model**: each page of the site is a class in `pages/`, so tests stay short and a site change is fixed in one place
- **pytest-html**: single-file HTML report
- **GitHub Actions**: CI pipeline running all browsers in parallel, on every push, every pull request, and weekly
- On failure: a screenshot, a video and a Playwright trace are saved automatically

## Project structure

```
brewdog-playwright-tests/
├── .github/workflows/playwright.yml   # CI pipeline
├── pages/                             # Page objects
│   ├── base_page.py                   # Shared actions: age gate, footer, layout checks
│   ├── home_page.py
│   ├── collection_page.py
│   ├── product_page.py
│   ├── search_page.py
│   └── cart_page.py
├── tests/                             # Test cases, grouped by area
├── conftest.py                        # Shared test setup
├── pytest.ini                         # Test settings
└── requirements.txt
```

## Running the tests locally

```bash
pip install -r requirements.txt
playwright install

pytest                       # all tests, Chromium, report in reports/report.html
pytest -m smoke              # only the quick smoke tests
pytest --browser firefox     # another browser
pytest --headed              # watch the browser while tests run
```

## Author

**Raphael Bouskila** – QA Engineer
[LinkedIn](https://www.linkedin.com/in/raphael-bouskila/) · [Portfolio & test reports](https://raphaelbouskila148-code.github.io/raphael-QA-HTML1/)
