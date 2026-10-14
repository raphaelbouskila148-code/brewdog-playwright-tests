from urllib.parse import quote_plus

from playwright.sync_api import Page

from pages.base_page import BasePage


class SearchPage(BasePage):
    """Search results page: /search?q=..."""

    def __init__(self, page: Page, query: str, product_only: bool = True):
        super().__init__(page)
        self.query = query
        # The site's own search box always adds type=product to the address.
        suffix = "&type=product" if product_only else ""
        self.URL = f"/search?q={quote_plus(query)}{suffix}"
        self.heading = page.locator("main h1").first
        self.no_results_message = page.locator("main").get_by_text("No results", exact=False).first

    @classmethod
    def search_from_header(cls, page: Page, query: str) -> "SearchPage":
        """Search the way a visitor does: type in the search box and press Enter."""
        box = page.locator("input[name='q']:visible").first
        box.click()
        box.fill(query)
        box.press("Enter")
        page.wait_for_url("**/search?**")
        return cls(page, query)
