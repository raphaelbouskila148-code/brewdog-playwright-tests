"""Product listing (collection) pages."""
import pytest
from playwright.sync_api import Page, expect

from pages.collection_page import CollectionPage

# Main shop categories from the site menu.
# @pytest.mark.parametrize runs the same test once per category.
COLLECTIONS = ["beer", "ipas", "lagers", "variety-packs", "non-alcoholics", "merch"]


@pytest.mark.smoke
@pytest.mark.parametrize("handle", COLLECTIONS)
def test_collection_page_lists_products(page: Page, handle: str):
    """TC-05 to TC-10: Each shop category opens and shows at least one product."""
    collection = CollectionPage(page, handle)
    response = page.goto(collection.URL)
    collection.confirm_age()

    assert response is not None and response.ok, f"/collections/{handle} returned an error"
    expect(collection.product_links().first).to_be_visible()


@pytest.mark.regression
def test_clicking_a_product_opens_its_page(page: Page):
    """TC-11: Clicking a product in the list opens that product's page."""
    collection = CollectionPage(page, "beer").open()
    product = collection.open_first_product()
    expect(product.title).to_be_visible()
