"""Homepage and age gate."""
import re

import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage

# Known issue found by this test suite (October 2026):
# the site has an age-confirmation popup built in, but its entry gate is
# switched off in the page settings (settings-entry-gate-enabled="false"),
# so new visitors are never asked to confirm their age.
# These tests are marked "xfail" (expected to fail) so the issue stays visible
# in every report without turning the whole run red. If BrewDog turns the gate
# back on, the tests will show as "XPASS" and the marker can be removed.
AGE_GATE_DISABLED = pytest.mark.xfail(
    reason="Known issue: age gate is disabled on the live site (entry gate setting is off)",
    strict=False,
)


@pytest.mark.smoke
def test_homepage_loads_with_correct_title(page: Page):
    """TC-01: Homepage opens and the browser tab shows the BrewDog title."""
    response = page.goto("/")
    assert response is not None and response.ok, "Homepage did not return a success status"
    expect(page).to_have_title(re.compile("BrewDog", re.IGNORECASE))


@pytest.mark.smoke
def test_age_gate_exists_on_page(page: Page):
    """TC-02: The age-confirmation popup with 'Confirm' and 'Cancel' is part of the page."""
    page.goto("/")
    gate = page.locator("uwp-age-gate, .age-gate").first
    expect(gate).to_be_attached()
    expect(gate.get_by_role("button", name="Confirm", exact=True, include_hidden=True)).to_be_attached()
    expect(gate.get_by_role("button", name="Cancel", exact=True, include_hidden=True)).to_be_attached()


@pytest.mark.regression
@AGE_GATE_DISABLED
def test_age_gate_is_shown_to_new_visitors(page: Page):
    """TC-03: A first-time visitor must confirm their age before browsing (alcohol retailer)."""
    home = HomePage(page).open(confirm_age=False)
    # The site's own setting delays the popup by up to 9.5 seconds, so allow 12.
    expect(home.age_gate_heading).to_be_visible(timeout=12_000)


@pytest.mark.regression
@AGE_GATE_DISABLED
def test_confirming_age_closes_the_age_gate(page: Page):
    """TC-04: Clicking 'Confirm' on the age gate closes it."""
    home = HomePage(page).open(confirm_age=False)
    home.age_confirm_button.click(timeout=12_000)
    expect(home.age_gate_heading).to_be_hidden()
