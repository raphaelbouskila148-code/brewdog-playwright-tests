"""Homepage and age gate."""
import re

import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage


@pytest.mark.smoke
def test_homepage_loads_with_correct_title(page: Page):
    """TC-01: Homepage opens and the browser tab shows the BrewDog title."""
    response = page.goto("/")
    assert response is not None and response.ok, "Homepage did not return a success status"
    expect(page).to_have_title(re.compile("BrewDog", re.IGNORECASE))


@pytest.mark.smoke
def test_age_gate_is_shown_to_new_visitors(page: Page):
    """TC-02: A first-time visitor must confirm their age before browsing (legal requirement)."""
    home = HomePage(page).open(confirm_age=False)
    expect(home.age_gate_heading).to_be_visible()
    expect(home.age_confirm_button).to_be_visible()


@pytest.mark.smoke
def test_confirming_age_closes_the_age_gate(page: Page):
    """TC-03: Clicking 'Confirm' closes the age gate."""
    home = HomePage(page).open(confirm_age=False)
    home.age_confirm_button.click()
    expect(home.age_gate_heading).to_be_hidden()


@pytest.mark.regression
def test_age_confirmation_is_remembered(page: Page):
    """TC-04: After confirming once, the age gate does not appear again on the next page."""
    HomePage(page).open()  # confirms age
    page.goto("/collections/beer")
    expect(page.get_by_text("Confirm your age")).to_be_hidden()
