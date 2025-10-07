"""Tests for the login page of Souper Saver."""

from unittest.mock import MagicMock, patch

from login import (sign_up_form,
                   login_page)


class TestSignUpForm:
    """Tests for the sign up form in the login page."""

    def test_sign_up_form_basic(self):
        """Test for sign_up_form to check it flows and signs users up correctly."""
        # Replace streamlit with a mock so no app runs during the tests
        with patch("login.st") as mock_st:

            # Mock the form
            mock_form = MagicMock()
            mock_form.text_input.side_effect = [
                "test_user", "test_user@sigmalabs.co.uk"]
            mock_form.form_submit_button.return_value = True
            mock_st.form.return_value.__enter__.return_value = mock_form

            # Mock database functions and is_valid_email as these have already been tested
            # and confirmed to work (test_login_functions.py)
            with patch("login.get_db_connection") as mock_db, \
                    patch("login.get_user_details") as mock_get_user, \
                    patch("login.is_valid_email") as mock_valid_email:

                # Mock the db connection
                mock_conn = MagicMock()
                mock_db.return_value = mock_conn

                # Mock that the inputted user wasn't found in the database
                mock_get_user.return_value = None

                # Mock that the email entered in the sign up was a valid format
                mock_valid_email.return_value = True

                # Run the sign_up_form function
                sign_up_form()

                # Assert if the database was called
                mock_get_user.assert_called_once()


class TestsLoginPage:
    """Tests for the login page."""

    def test_login_page(self):
        """Test for login_page which checks if user enters a valid 
        email then it shows it already exists in the database"""
        # Replace streamlit with a mock so no app runs during the tests
        with patch('login.st') as mock_st:

            # Mock the form
            mock_form = MagicMock()
            mock_form.text_input.return_value = "test_user@sigmalabs.co.uk"
            mock_form.form_submit_button.return_value = True
            mock_st.form.return_value.__enter__.return_value = mock_form

            # Mock database functions and is_valid_email as these have already been tested
            # and confirmed to work (test_login_functions.py)
            with patch("login.get_db_connection") as mock_db, \
                    patch("login.get_user_details") as mock_get_user, \
                    patch("login.is_valid_email") as mock_valid_email, \
                    patch("login.verify_user_password") as mock_verify_user:

                # Mock the db connection
                mock_conn = MagicMock()
                mock_db.return_value = mock_conn

                # Mock a user and set their username
                mock_user = MagicMock()
                mock_user.user_name = "test_user"

                # Mock returning a valid and verified user
                mock_get_user.return_value = mock_user
                mock_verify_user = True

                # Set the email to be of a valid format
                mock_valid_email.return_value = True

                # Mock session state
                mock_session = MagicMock()
                mock_st.session_state = mock_session

                # Run the login_page function
                login_page()

                # Assert if a valid user was successfully logged in
                assert mock_session.user == mock_user
                assert mock_session.logged_in is True
