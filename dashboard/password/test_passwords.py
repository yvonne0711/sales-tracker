"""Tests for the passwords.py script."""

from unittest.mock import MagicMock, patch
from argon2 import PasswordHasher

from passwords import verify_user_password


def test_verify_user_success():
    """Test when password is correct."""
    mock_conn = MagicMock()
    ph = PasswordHasher()
    hashed = ph.hash("correct_password")
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'password_hash': hashed}
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    result = verify_user_password(mock_conn, "test_user", "correct_password")
    assert result is True


def test_verify_user_fail():
    """Test when password is correct."""
    mock_conn = MagicMock()
    ph = PasswordHasher()
    hashed = ph.hash("correct_password")
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'password_hash': hashed}
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    result = verify_user_password(mock_conn, "test_user", "wrong_password")
    assert result is False
