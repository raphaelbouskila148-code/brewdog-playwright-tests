"""
BasePage: the parent class for every page object.

Page Object Model (POM): each page of the site gets its own class that knows
HOW to find things on that page (locators) and HOW to do things there
(actions). Tests then only describe WHAT to check. If the site changes a
button, we fix it in one place here instead of in every test.
"""
import re

from playwright.sync_api import Locator, Page, TimeoutError as PlaywrightTimeoutError


class BasePage:
    # Path of the page, relative to base_url in pytest.ini
    URL = "/"

    def __init__(self, page: Page):
        self.page = page

        # Age gate shown on first visit ("Confirm your age")
        self.age_gate_heading = page.get_by_text("Confirm your age")
        self.age_confirm_button = page.get_by_role("button", name="Confirm", exact=True)

        # Header and footer exist on every page
        self.search_button = page.get_by_label("Access Search").first
        self.footer = page.locator("footer")

    # ---------- actions ----------

    def open(self, confirm_age: bool = True):
        """Go to this page. By default, also get past the age gate."""
        self.page.goto(self.URL)
        if confirm_age:
            self.confirm_age()
        return self

    def confirm_age(self):
        """Click 'Confirm' on the age gate if it appears."""
        self._click_if_visible(self.age_confirm_button)

    # ---------- helpers ----------

    def footer_link(self, name: str) -> Locator:
        return self.footer.get_by_role("link", name=name, exact=True).first

    def has_horizontal_scroll(self) -> bool:
        """True if the page is wider than the screen (a common mobile layout bug)."""
        return self.page.evaluate(
            "() => document.documentElement.scrollWidth > window.innerWidth + 1"
        )

    def product_links(self) -> Locator:
        """All links that lead to a product page."""
        return self.page.locator("main a[href*='/products/']")

    @staticmethod
    def _click_if_visible(locator: Locator, timeout: int = 5000) -> bool:
        """Click an element only if it shows up within `timeout` ms.

        Popups such as the age gate do not always appear, so a missing popup
        should not fail the test.
        """
        try:
            locator.click(timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False


PRICE_PATTERN = re.compile(r"\$\s?\d+(\.\d{2})?")
