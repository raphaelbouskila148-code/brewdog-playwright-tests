"""Search."""
import pytest
from playwright.sync_api import Page, expect

from pages.search_page import SearchPage


@pytest.mark.smoke
def test_search_for_ipa_returns_products(page: Page):
    """TC-15: Searching 'IPA' returns product results."""
    search = SearchPage(page, "IPA").open()
    expect(search.product_links().first).to_be_visible()


@pytest.mark.regression
def test_search_with_no_matches_shows_message(page: Page):
    """TC-16: A search with no matches tells the user nothing was found."""
    search = SearchPage(page, "zzqxnotarealbeer").open()
    expect(search.no_results_message).to_be_visible()


@pytest.mark.regression
def test_no_results_message_shows_search_term(page: Page):
    """TC-17: The 'no results' message repeats what the user typed,
    and does not show an unfilled template placeholder like {{terms}}."""
    term = "zzqxnotarealbeer"
    search = SearchPage(page, term).open()
    expect(search.no_results_message).to_be_visible()
    expect(search.no_results_message).not_to_contain_text("{{")
