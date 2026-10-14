"""Mobile layout, tested on an emulated iPhone screen."""
import pytest
from playwright.sync_api import Browser, Playwright, expect

from pages.collection_page import CollectionPage
from pages.home_page import HomePage


@pytest.fixture
def mobile_page(playwright: Playwright, browser: Browser, base_url: str):
    """A browser tab that looks to the site like an iPhone 13."""
    iphone = dict(playwright.devices["iPhone 13"])
    # Firefox can't emulate phone touch screens, so drop those settings there
    if browser.browser_type.name == "firefox":
        iphone.pop("is_mobile", None)
        iphone.pop("has_touch", None)
    context = browser.new_context(**iphone, base_url=base_url, locale="en-US")
    page = context.new_page()
    yield page
    context.close()


@pytest.mark.mobile
def test_homepage_fits_mobile_screen(mobile_page):
    """TC-25: On mobile, the homepage fits the screen with no sideways scrolling."""
    home = HomePage(mobile_page).open()
    assert not home.has_horizontal_scroll(), "Homepage is wider than the phone screen"


@pytest.mark.mobile
def test_collection_page_works_on_mobile(mobile_page):
    """TC-26: On mobile, a shop category shows products and fits the screen."""
    collection = CollectionPage(mobile_page, "beer").open()
    expect(collection.product_links().first).to_be_visible()
    assert not collection.has_horizontal_scroll(), "Category page is wider than the phone screen"
