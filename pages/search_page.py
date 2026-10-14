from urllib.parse import quote_plus

from playwright.sync_api import Page

from pages.base_page import BasePage


class SearchPage(BasePage):
    """Search results page: /search?q=..."""

    def __init__(self, page: Page, query: str):
        super().__init__(page)
        self.query = query
        self.URL = f"/search?q={quote_plus(query)}"
        self.no_results_message = page.get_by_text("No results found", exact=False).first
