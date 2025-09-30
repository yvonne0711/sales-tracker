"""Tests for the skeleton of the dashboard."""

from skeleton_dashboard import is_valid_email

def test_is_valid_email_returns_bool():
    """Tests if the is_valid_email function returns a bool."""
    valid = "test_user@sigmalabs.co.uk"
    invalid = "test_user.co.uk"
    assert is_valid_email(valid) is True
    assert is_valid_email(invalid) is False

