from playwright.sync_api import Page

from pages.base_page import BasePage


class CollectionPage(BasePage):
    """A product listing page, e.g. /collections/ipas."""

    def __init__(self, page: Page, handle: str):
        super().__init__(page)
        self.handle = handle
        self.URL = f"/collections/{handle}"

    def open_first_product(self):
        """Click the first product in the list and return the product page."""
        from pages.product_page import ProductPage

        self.product_links().first.click()
        self.page.wait_for_url("**/products/**")
        return ProductPage(self.page)
