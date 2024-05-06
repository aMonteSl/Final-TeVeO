from django.test import TestCase, RequestFactory
import unittest
import os
from xml.dom.minidom import parseString
# RequestFactory se usa para crear request falsos
from . import manageUser
from . import manageOrder
from . import manageMedia
from . import views
from .models import Camera, Comment


class TestViews(TestCase):

    def test_index(self):
        # Hay que crear un request falso con RequestFactory con una sesion falsa para que no de error al ejecutar la vista
        # la sesion tiene un username, font_size, font_family y token que son necesarios para que no de error al ejecutar la vista index en views.py 
        request = RequestFactory().get('/')
        request.session = {'username': '', 'font_size': 'TEST', 'font_family': 'TEST'}
        response = views.index(request)
        print("Test index")
        self.assertEqual(response.status_code, 200)

    def test_mainCameras(self):
        request = RequestFactory().get('/camaras/')
        request.session = {'username': '', 'font_size': 'TEST', 'font_family': 'TEST'}
        response = views.mainCameras(request)
        print("Test mainCameras")
        self.assertEqual(response.status_code, 200)
    
    def test_camera(self):
        # Creamos una camara con el id TEST
        cam = Camera.objects.create(source_id='TEST', id='TEST', src='TEST', name='TEST', coordinates='TEST', img_path='TEST')
        # Guardamos la camara
        cam.save()
        # Creamos un request con el id TEST
        request = RequestFactory().get('/camaras/TEST/')
        request.session = {'username': '', 'font_size': 'TEST', 'font_family': 'TEST'}
        response = views.camera(request, 'TEST')
        self.assertEqual(response.status_code, 200)
        print("Test camera")
        # Borramos la camara
        cam.delete()

    def test_save_comment_if_post(self):
        # Creamos una camara con el id TEST
        cam = Camera.objects.create(source_id='TEST', id='TEST', src='TEST', name='TEST', coordinates='TEST', img_path='TEST')
        # Guardamos la camara
        cam.save()
        # Creamos un request POST con el id TEST y un cuerpo de comentario
        request = RequestFactory().post('/camaras/TEST/', {'body': 'This is a test comment'})
        request.session = {'username': '', 'font_size': 'TEST', 'font_family': 'TEST'}
        # Llamamos al método save_comment_if_post
        views.save_comment_if_post(request, cam, 'TEST')
        # Verificamos que el comentario se haya guardado correctamente
        comment = Comment.objects.get(camera=cam)
        self.assertEqual(comment.comment, 'This is a test comment')
        print("Test save_comment_if_post")
        # Borramos la camara y el comentario
        comment.delete()
        cam.delete()
