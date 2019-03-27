from django.test import TestCase

from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_address_successfully(self):
        """
        test creating a new user with an email address is successful
        :return:
        """
        email = "test@example.com"
        password = "testexamplepassword"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        test the email address for a new user is normalized
        :return:
        """

        email = "asd@eXAMPlE.com"
        user = get_user_model().objects.create_user(email, "asdas@123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        test creating user with no email address raises error
        :return:
        """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "asd123")

    def test_create_new_superuser(self):
        """
        test creating a new superuser
        :return:
        """

        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test13333"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
