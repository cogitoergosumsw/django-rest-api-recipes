from unittest.mock import patch
from django.test import TestCase

from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@example.com', password='testpassword'):
    """
    create sample user
    :param email:
    :param password:
    :return:
    """
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """
        test the tag string representation
        :return:
        """

        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vaegan"
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """
        test the ingredient string representation
        :return:
        """
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """
        test the recipe string representation
        :return:
        """
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and Mushroom sauce',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """
        test that image is saved in the correct location
        :return:
        """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid

        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
