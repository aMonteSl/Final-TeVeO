from django.test import TestCase, Client
from .views import *
from .manageUser import *
# Create your tests here.

# Tengo que hacer test unitarios(prueba de metodos) y extremo a
# extremo(los que simulan peticiones get/post)

# Test a todos los metodos de manageUser.py


class TestManageUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.request = self.client.get('/')
        self.request.session['username'] = "Pepe"
        self.request.session['font_size'] = "small"
        self.request.session['font_family'] = "Verdana"
        get_user_config(self.request)

    def test_manageNameLogin(self):
        self.assertEqual(manageNameLogin(self.request), "Pepe")
        self.request.session['username'] = ""
        self.assertEqual(manageNameLogin(self.request), DEFAULT_NAME)
        self.request.session['username'] = None
        self.assertEqual(manageNameLogin(self.request), DEFAULT_NAME)

    def test_manageSize(self):
        self.assertEqual(manageSize(self.request), "font-size-pequena")
        self.request.session['font_size'] = "large"
        self.assertEqual(manageSize(self.request), "font-size-grande")
        self.request.session['font_size'] = "medium"
        self.assertEqual(manageSize(self.request), DEFAULT_FONT_SIZE)
        self.request.session['font_size'] = None
        self.assertEqual(manageSize(self.request), DEFAULT_FONT_SIZE)
        manageSize(self.request)

    def test_manageFamily(self):
        self.assertEqual(manageFamily(self.request), "font-family-verdana")
        self.request.session['font_family'] = "Courier New"
        self.assertEqual(manageFamily(self.request), "font-family-courier")
        self.request.session['font_family'] = "Verdana"
        self.assertEqual(manageFamily(self.request), "font-family-verdana")
        self.request.session['font_family'] = "Times New Roman"
        self.assertEqual(manageFamily(self.request), "font-family-times")
        self.request.session['font_family'] = "Helvetica"
        self.assertEqual(manageFamily(self.request), "font-family-helvetica")
        self.request.session['font_family'] = "Arial"
        self.assertEqual(manageFamily(self.request), "font-family-arial")
        self.request.session['font_family'] = "C4 Type"
        self.assertEqual(manageFamily(self.request), "font-family-c4type")
        self.request.session['font_family'] = None
        self.assertEqual(manageFamily(self.request), DEFAULT_FONT_FAMILY)
        manageFamily(self.request)
