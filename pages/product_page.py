import re

from playwright.sync_api import Page

from pages.base_page import PRICE_PATTERN, BasePage


class ProductPage(BasePage):
    """A single product page, e.g. /products/non-alcoholic-mix-pack."""

    def __init__(self, page: Page, handle: str | None = None):
        super().__init__(page)
        if handle:
            self.URL = f"/products/{handle}"

        self.title = page.locator("main h1").first
        self.price = page.locator("main").get_by_text(PRICE_PATTERN).first
        # The site says "basket" in some places, so accept either word
        self.add_to_cart_button = page.get_by_role(
            "button", name=re.compile(r"add to (cart|basket)", re.IGNORECASE)
        ).first

        # Quantity "+" buttons. On BrewDog the quantity starts at 0, so a
        # customer has to press "+" before "Add to basket" adds anything.
        self.increase_quantity_button = page.locator("main").get_by_role(
            "button", name="Increase quantity"
        ).first

    def add_to_cart(self, quantity: int = 1):
        """Choose a quantity with the '+' button (if the page has one), then add to basket."""
        if self.increase_quantity_button.is_visible():
            for _ in range(quantity):
                self.increase_quantity_button.click()
        self.add_to_cart_button.click()
