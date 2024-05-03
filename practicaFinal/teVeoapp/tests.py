from django.test import TestCase, RequestFactory 
# RequestFactory se usa para crear request falsos
from . import manageUser
from . import views

class ManageUserTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_manageNameLogin(self):
        request = self.factory.get('/')
        request.session = {'username': 'TestUser'}
        self.assertEqual(manageUser.manageNameLogin(request), 'TestUser')

        request.session = {'username': ''}
        self.assertEqual(manageUser.manageNameLogin(request), manageUser.DEFAULT_NAME)

        request.session = {}
        self.assertEqual(manageUser.manageNameLogin(request), manageUser.DEFAULT_NAME)

    def test_manageSize(self):
        request = self.factory.get('/')
        request.session = {'font_size': 'small'}
        self.assertEqual(manageUser.manageSize(request), 'font-size-pequena')

        request.session = {'font_size': 'large'}
        self.assertEqual(manageUser.manageSize(request), 'font-size-grande')

        request.session = {'font_size': 'medium'}
        self.assertEqual(manageUser.manageSize(request), manageUser.DEFAULT_FONT_SIZE)

        request.session = {}
        self.assertEqual(manageUser.manageSize(request), manageUser.DEFAULT_FONT_SIZE)

    def test_manageFamily(self):
        request = self.factory.get('/')
        request.session = {'font_family': 'Courier New'}
        self.assertEqual(manageUser.manageFamily(request), 'font-family-courier')

        request.session = {'font_family': 'Verdana'}
        self.assertEqual(manageUser.manageFamily(request), 'font-family-verdana')

        request.session = {'font_family': 'Times New Roman'}
        self.assertEqual(manageUser.manageFamily(request), 'font-family-times')

        request.session = {'font_family': 'Helvetica'}
        self.assertEqual(manageUser.manageFamily(request), 'font-family-helvetica')

        request.session = {'font_family': 'Arial'}
        self.assertEqual(manageUser.manageFamily(request), 'font-family-arial')

        request.session = {'font_family': 'C4 Type'}
        self.assertEqual(manageUser.manageFamily(request), 'font-family-c4type')

        request.session = {'font_family': 'Roboto'}
        self.assertEqual(manageUser.manageFamily(request), manageUser.DEFAULT_FONT_FAMILY)

        request.session = {}
        self.assertEqual(manageUser.manageFamily(request), manageUser.DEFAULT_FONT_FAMILY)

    def test_get_user_config(self):
        request = self.factory.get('/')
        request.session = {'username': 'TestUser', 'font_size': 'small', 'font_family': 'Courier New'}
        self.assertEqual(manageUser.get_user_config(request), ('TestUser', 'font-size-pequena', 'font-family-courier'))