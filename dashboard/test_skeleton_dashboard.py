"""Tests for the skeleton of the dashboard."""
import os

import pytest
from unittest.mock import Mock, patch, MagicMock
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from skeleton_dashboard import (get_db_connection,
                                get_user_details,
                                select_website_id,
                                insert_product_details,
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


class TestUserDetails:

    def test_get_user_details_gives_expected_output(self):
        """Tests if the get user details function is successful."""
        mock_conn = MagicMock()

        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value

        expected_data = {"user_id": 1, "user_email": "test_user@sigmalabs.co.uk"}
        mock_cursor.fetchone.return_value = expected_data

        result = get_user_details(mock_conn, "test_user@sigmalabs.co.uk")

        mock_cursor.execute.assert_called_once_with(
            """
                SELECT *
                FROM users
                WHERE user_email = (%s);
                """,
            ("test_user@sigmalabs.co.uk",)
        )
        assert result == expected_data


    def test_get_user_details_failed_output(self):
        """Tests if the get user details returns None for no user found."""
        mock_conn = MagicMock()

        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value

        mock_cursor.fetchone.return_value = None

        result = get_user_details(mock_conn, "test_user@sigmalabs.co.uk")

        mock_cursor.execute.assert_called_once_with(
            """
                SELECT *
                FROM users
                WHERE user_email = (%s);
                """,
            ("test_user@sigmalabs.co.uk",)
        )
        assert result is None



class TestWebsiteFunctions:

    def test_select_website_id_gives_expected_output(self):
        """Tests if the select website id function successfully retrieves an id."""
        mock_conn = MagicMock()
        
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        
        expected_data = {"website_id": 1}
        mock_cursor.fetchone.return_value = expected_data

        result = select_website_id(mock_conn, "Steam")
        
        mock_cursor.execute.assert_called_once_with(
            """
                SELECT website_id
                FROM website
                WHERE website_name = (%s);
                """,
            ("steam",)
        )
        assert result == expected_data

    def test_select_website_id_failed_output(self):
        """Tests if the select website id function returns None for no user found."""
        mock_conn = MagicMock()

        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value

        mock_cursor.fetchone.return_value = None

        result = select_website_id(mock_conn, "Steam")

        mock_cursor.execute.assert_called_once_with(
            """
                SELECT website_id
                FROM website
                WHERE website_name = (%s);
                """,
            ("steam",)
        )
        assert result is None


class TestProductFunctions:

    def test_insert_product_details_gives_expected_output(self):
        """Tests if the insert product details function successfully retrieves an id."""
        mock_conn = MagicMock()

        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value

        expected_data = 123
        mock_cursor.fetchone.return_value = {"product_id": expected_data}

        result = insert_product_details(mock_conn, "test product", "http://test_website.co.uk", 1)

        mock_cursor.execute.assert_called_once_with(
            """
                INSERT INTO product
                    (product_name, product_url, website_id)
                VALUES
                    (%s, %s, %s)
                RETURNING product_id;
                """,
            ("test product", "http://test_website.co.uk", 1)
        )
        assert result == expected_data




class TestEmailValidation:

    def test_is_valid_email_returns_bool(self):
        """Tests if the is_valid_email function returns a bool."""
        valid = "test_user@sigmalabs.co.uk"
        invalid = "test_user.co.uk"
        assert is_valid_email(valid) is True
        assert is_valid_email(invalid) is False

