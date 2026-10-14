"""
Shared pytest fixtures.

pytest-playwright already gives every test a fresh `page` (a new browser tab
with clean cookies). The fixtures here add project settings on top of that and
hand tests a ready-to-use page object.
"""
import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Make every test behave like a desktop visitor from the US."""
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "locale": "en-US",
        "timezone_id": "America/New_York",
    }


@pytest.fixture
def home(page: Page) -> HomePage:
    """Homepage, opened and with the age gate already confirmed."""
    return HomePage(page).open()
