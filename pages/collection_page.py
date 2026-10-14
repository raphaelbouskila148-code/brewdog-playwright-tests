from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage


class CollectionPage(BasePage):
    """A product listing page, e.g. /collections/ipas."""

    def __init__(self, page: Page, handle: str):
        super().__init__(page)
        self.handle = handle
        self.URL = f"/collections/{handle}"

    def product_paths(self) -> list[str]:
        """Addresses of the products listed on this page, without duplicates."""
        self.product_links().first.wait_for()
        return self.page.eval_on_selector_all(
            "main a[href*='/products/']",
            "els => [...new Set(els.map(e => e.getAttribute('href').split('?')[0]))]",
        )

    def open_first_product(self):
        """Click the first product in the list and return the product page."""
        from pages.product_page import ProductPage

        self.product_links().first.click()
        self.page.wait_for_url("**/products/**")
        return ProductPage(self.page)

    def open_first_buyable_product(self, max_products: int = 8):
        """Open the first product that can actually be added to the cart.

        Some products are "Sold out", and beer is not sold online in the US
        (those pages show "Find Near You" instead), so we skip past those.
        """
        from pages.product_page import ProductPage

        for path in self.product_paths()[:max_products]:
            self.page.goto(path)
            product = ProductPage(self.page)
            try:
                product.add_to_cart_button.wait_for(state="visible", timeout=5000)
            except PlaywrightTimeoutError:
                continue  # sold out or not sold online, try the next one
            if product.add_to_cart_button.is_enabled():
                return product
        raise AssertionError(f"No in-stock product found in /collections/{self.handle}")
