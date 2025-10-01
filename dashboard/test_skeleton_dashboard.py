"""Tests for the skeleton of the dashboard."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from skeleton_dashboard import (get_db_connection,
                                get_user_details,
                                is_valid_email)


@pytest.fixture
def mock_env_file():
    """Fixture that mocks the environment variables."""
    return {
        "DB_USERNAME": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "test_database"
    }

class TestsDatabaseFunctions:
    # Create patch for connection and .env file
    @patch("skeleton_dashboard.psycopg2.connect")
    def test_get_db_connection_is_successful(self, mock_connect, mock_env_file):
        """Tests if database connection is successful."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        with patch.dict("skeleton_dashboard.ENV", mock_env_file):
            result = get_db_connection()

        mock_connect.assert_called_once_with(
            user="test_user",
            password= "test_password",
            host= "localhost",
            port="5432",
            database= "test_database",
            cursor_factory=RealDictCursor
        )

        assert result == mock_conn

    @patch("skeleton_dashboard.psycopg2.connect")
    def test_get_db_connection_when_fails(self, mock_connect, mock_env_file):
        """Tests the connection returns none if unsuccessful."""
        mock_connect.side_effect = Error("Connection Failed")

        with patch.dict("skeleton_dashboard.ENV", mock_env_file):
            result = get_db_connection()

        assert result is None


class TestEmailValidation:

    def test_is_valid_email_returns_bool(self):
        """Tests if the is_valid_email function returns a bool."""
        valid = "test_user@sigmalabs.co.uk"
        invalid = "test_user.co.uk"
        assert is_valid_email(valid) is True
        assert is_valid_email(invalid) is False

