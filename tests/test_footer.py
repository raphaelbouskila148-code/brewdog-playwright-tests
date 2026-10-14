"""Footer links."""
import pytest
from playwright.sync_api import expect

# (link text, part of the address it should point to)
FOOTER_LINKS = [
    ("Shipping & Returns", "shipping-returns"),
    ("FAQs & Contact Us", "contact-us"),
    ("Terms & Conditions", "terms-and-conditions"),
    ("Privacy Policy", "privacy-policy"),
]


@pytest.mark.smoke
@pytest.mark.parametrize("link_text, expected_path", FOOTER_LINKS)
def test_footer_link_points_to_correct_page(home, link_text: str, expected_path: str):
    """TC-21 to TC-24: Key footer links exist and point to the right page."""
    link = home.footer_link(link_text)
    expect(link).to_be_attached()
    href = link.get_attribute("href") or ""
    assert expected_path in href, f"'{link_text}' points to {href!r}"
