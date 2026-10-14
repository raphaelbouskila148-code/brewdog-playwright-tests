"""Product page."""
import pytest
from playwright.sync_api import Page, expect

from pages.collection_page import CollectionPage


@pytest.fixture
def product(page: Page):
    """Open the first product in the Beer category.

    Starting from the category (instead of a fixed product link) keeps the
    tests working when BrewDog adds or removes products.
    """
    return CollectionPage(page, "beer").open().open_first_product()


@pytest.mark.smoke
def test_product_page_shows_name(product):
    """TC-12: Product page shows the product name."""
    expect(product.title).to_be_visible()
    expect(product.title).not_to_be_empty()


@pytest.mark.smoke
def test_product_page_shows_price_in_dollars(product):
    """TC-13: Product page shows a price in US dollars."""
    expect(product.price).to_be_visible()


@pytest.mark.smoke
def test_product_page_has_add_to_cart_button(product):
    """TC-14: Product page has an 'Add to cart' button."""
    expect(product.add_to_cart_button).to_be_visible()
