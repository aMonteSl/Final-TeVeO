from django.test import TestCase, RequestFactory
import unittest
import os
from xml.dom.minidom import parseString
# RequestFactory se usa para crear request falsos
from . import manageUser
from . import manageOrder
from manageMedia import *
from . import views
from .models import Camera, Comment


class TestViews(TestCase):

    def test_index(self):
        request = RequestFactory().get('/caras/')
        response = views.index(request)
        self.assertEqual(response.status_code, 200)

    def test_mainCameras(self):
        request = RequestFactory().get('/camaras/')
        response = views.mainCameras(request)
        self.assertEqual(response.status_code, 200)

    def test_camera(self):
        # Creamos una camara con el id TEST
        cam = Camera.objects.create(id='TEST', name='TEST',
                                    url='TEST', user='TEST', password='TEST')
        # Guardamos la camara
        cam.save()
        # Creamos un request con el id TEST
        request = RequestFactory().get('/camaras/TEST/')
        response = views.camera(request, 'TEST')
        self.assertEqual(response.status_code, 200)
        # Borramos la camara
        cam.delete()
