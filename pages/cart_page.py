import re

from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "/cart"

    def item_count(self) -> int:
        """Number of items in the cart, read from Shopify's cart API.

        `page.request` shares cookies with the browser, so this returns the
        same cart the user sees. Checking the API is more reliable than
        reading the number from the cart icon.
        """
        response = self.page.request.get("/cart.js")
        assert response.ok, f"/cart.js returned {response.status}"
        return response.json()["item_count"]

    def wait_for_items(self, minimum: int = 1, timeout_ms: int = 10_000) -> int:
        """Check the cart every half second until it has `minimum` items.

        Adding to cart happens in the background, so we wait for it instead of
        checking once and failing too early. Returns the final count.
        """
        waited = 0
        count = self.item_count()
        while count < minimum and waited < timeout_ms:
            self.page.wait_for_timeout(500)
            waited += 500
            count = self.item_count()
        return count

    @property
    def empty_message(self):
        return self.page.get_by_text(re.compile(r"empty", re.IGNORECASE)).first
