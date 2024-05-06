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

    def try_index(self):
        request = RequestFactory().get('/')
        response = views.index(request)
        self.assertEqual(response.status_code, 200)

    def try_mainCameras(self):
        request = RequestFactory().get('/camaras/')
        response = views.mainCameras(request)
        self.assertEqual(response.status_code, 200)

    def try_camera(self):
        # Creamos una camara con el id TRY
        cam = Camera.objects.create(id='TRY', name='TRY', url='TRY', user='TRY', password='TRY')
        # Guardamos la camara
        cam.save()
        # Creamos un request con el id TRY
        request = RequestFactory().get('/camaras/TRY/')
        response = views.camera(request, 'TRY')
        self.assertEqual(response.status_code, 200)
        # Borramos la camara
        cam.delete()