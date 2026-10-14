"""Search."""
import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.search_page import SearchPage


@pytest.mark.smoke
def test_search_box_returns_products_for_ipa(page: Page):
    """TC-15: Typing 'IPA' in the search box and pressing Enter shows product results."""
    HomePage(page).open()
    search = SearchPage.search_from_header(page, "IPA")
    expect(search.heading).to_contain_text("IPA", ignore_case=True)
    expect(search.product_links().first).to_be_visible()


# Bug found by this suite (October 2026): /search?q=IPA without "type=product"
# never shows results. The page's product data is not valid JSON (one product
# has an empty "available" value), so the script that draws the results crashes
# and the page stays on loading placeholders. Shared or bookmarked search links
# are affected; the search box is not, because it adds type=product.
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known bug: search results page crashes without type=product (invalid product JSON)",
    strict=False,
)
def test_search_link_without_type_shows_results(page: Page):
    """TC-16: A plain search link (/search?q=IPA) shows product results."""
    search = SearchPage(page, "IPA", product_only=False).open()
    expect(search.product_links().first).to_be_visible(timeout=10_000)


# Bug found by this suite (October 2026): a search with no matches shows a list
# of unrelated products and no message saying nothing was found.
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known issue: no-match search shows unrelated products and no 'no results' message",
    strict=False,
)
def test_search_with_no_matches_tells_user(page: Page):
    """TC-17: A search with no matches tells the user nothing was found."""
    search = SearchPage(page, "zzqxnotarealbeer").open()
    expect(search.no_results_message).to_be_visible()
