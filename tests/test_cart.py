"""Cart.

These tests never go to checkout or place an order. They only add an item to
the cart and check that it arrived.
"""
import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.collection_page import CollectionPage


@pytest.mark.smoke
def test_new_visitor_cart_is_empty(page: Page):
    """TC-18: A new visitor starts with an empty cart."""
    cart = CartPage(page).open()
    assert cart.item_count() == 0
    expect(cart.empty_message).to_be_visible()


@pytest.mark.regression
def test_add_product_to_cart(page: Page):
    """TC-19: Adding an in-stock product from its page puts it in the cart."""
    product = CollectionPage(page, "non-alcoholics").open().open_first_buyable_product()
    cart = CartPage(page)
    assert cart.item_count() == 0

    product.add_to_cart()

    assert cart.wait_for_items(1) >= 1, "Item was not added to the cart"


@pytest.mark.regression
def test_added_product_appears_on_cart_page(page: Page):
    """TC-20: The product added to the cart is listed on the cart page."""
    product = CollectionPage(page, "non-alcoholics").open().open_first_buyable_product()
    name = product.title.inner_text().strip()
    product.add_to_cart()
    cart = CartPage(page)
    cart.wait_for_items(1)

    cart.open()
    expect(page.locator("main")).to_contain_text(name, ignore_case=True)
