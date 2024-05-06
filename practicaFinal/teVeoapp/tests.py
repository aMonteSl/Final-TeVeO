from django.test import TestCase, RequestFactory
# RequestFactory se usa para crear request falsos
from . import manageUser
from . import manageOrder
from . import views
from .models import Camera, Comment


class TestExtremeoExtremo(TestCase):

    def test_index(self):
        # Hay que crear un request falso con RequestFactory
        # con una sesion falsa para que no de error al ejecutar la vista
        # la sesion tiene un username, font_size, font_family y
        # token que son necesarios para que no de error al ejecutar la vista
        # index en views.py
        request = RequestFactory().get('/')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.index(request)
        print("Test index")
        self.assertEqual(response.status_code, 200)

    def testConfig(self):
        request = RequestFactory().get('/config/')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.config(request)
        print("Test config")
        self.assertEqual(response.status_code, 200)

    def test_help(self):
        request = RequestFactory().get('/ayuda/')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.help(request)
        print("Test help")
        self.assertEqual(response.status_code, 200)

    def test_mainCameras(self):
        request = RequestFactory().get('/camaras/')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.mainCameras(request)
        print("Test mainCameras")
        self.assertEqual(response.status_code, 200)

    def test_cameras_json(self):
        request = RequestFactory().get('/camaras/json')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.cameras_json(request)
        print("Test cameras_json")
        self.assertEqual(response.status_code, 200)

    def test_camera(self):
        # Creamos una camara con el id TEST
        cam = Camera.objects.create(source_id='TEST', id='TEST',
                                    src='https://infocar.dgt.es/etraffic/data/camaras/4.jpg', name='TEST',
                                    coordinates='TEST', img_path='TEST')
        # Guardamos la camara
        cam.save()
        # Creamos un request con el id TEST
        request = RequestFactory().get('/camaras/TEST/')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.camera(request, 'TEST')
        self.assertEqual(response.status_code, 200)
        print("Test camera")
        # Borramos la camara
        cam.delete()

    def test_comment_view_get(self):
        request = RequestFactory().get('/comentario/')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.comment_view(request)
        self.assertEqual(response.status_code, 200)
        print("Test comment_view_get")

    def test_camera_json(self):
        # Creamos una camara con el id TEST
        cam = Camera.objects.create(source_id='TEST', id='TEST',
                                    src='https://infocar.dgt.es/etraffic/data/camaras/4.jpg', name='TEST',
                                    coordinates='TEST', img_path='TEST')
        # Guardamos la camara
        cam.save()
        # Creamos un request con el id TEST
        request = RequestFactory().get('/camaras/TEST/json')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.camera_json(request, 'TEST')
        self.assertEqual(response.status_code, 200)
        print("Test camera_json")
        # Borramos la camara
        cam.delete()

    def test_camera_dyn(self):
        # Creamos una camara con el id TEST
        cam = Camera.objects.create(source_id='TEST', id='TEST',
                                    src='https://infocar.dgt.es/etraffic/data/camaras/4.jpg', name='TEST',
                                    coordinates='TEST', img_path='TEST')
        # Guardamos la camara
        cam.save()
        # Creamos un request con el id TEST
        request = RequestFactory().get('/camaras/TEST/dyn')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.camera_dyn(request, 'TEST')
        self.assertEqual(response.status_code, 200)
        print("Test camera_dyn")
        # Borramos la camara
        cam.delete()

    def test_latest_image(self):
        # Creamos una camara con el id TEST
        cam = Camera.objects.create(source_id='TEST', id='TEST',
                                    src='https://infocar.dgt.es/etraffic/data/camaras/4.jpg', name='TEST',
                                    coordinates='TEST', img_path='TEST')
        # Guardamos la camara
        cam.save()

        # Creamos un request con el id TEST
        request = RequestFactory().get('/camaras/TEST/img')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.latest_image(request, 'TEST')
        self.assertEqual(response.status_code, 200)
        print("Test latest_image")
        # Borramos la camara
        cam.delete()

    def test_get_comments(self):
        # Creamos una camara con el id TEST
        cam = Camera.objects.create(source_id='TEST', id='TEST',
                                    src='https://infocar.dgt.es/etraffic/data/camaras/4.jpg', name='TEST',
                                    coordinates='TEST', img_path='TEST')
        # Guardamos la camara
        cam.save()

        # Creamos un comentario para la camara
        comment = Comment.objects.create(
            name='TEST',
            camera=cam,
            comment='TEST-TEST',
            date='06-04-24',
            img_path_comment='TEST')
        # Guardamos el comentario
        comment.save()

        # Creamos un request con el id TEST
        request = RequestFactory().get('/camaras/TEST/comment')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.get_comments(request, 'TEST')
        self.assertEqual(response.status_code, 200)
        print("Test get_comments")
        # Borramos la camara
        cam.delete()


class TestManageUser(TestCase):
    def test_manageNameLogin_empty(self):
        request = RequestFactory().get('/')
        request.session = {'username': ''}
        response = manageUser.manageNameLogin(request)
        self.assertEqual(response, manageUser.DEFAULT_NAME)

    def test_manageNameLogin_none(self):
        request = RequestFactory().get('/')
        request.session = {'username': None}
        response = manageUser.manageNameLogin(request)
        self.assertEqual(response, manageUser.DEFAULT_NAME)
        print("Test manageNameLogin_empty")

    def test_manageNameLogin_name(self):
        request = RequestFactory().get('/')
        request.session = {'username': 'TEST'}
        response = manageUser.manageNameLogin(request)
        self.assertEqual(response, 'TEST')
        print("Test manageNameLogin_name")

    def test_manageSize_small(self):
        request = RequestFactory().get('/')
        request.session = {'font_size': 'small'}
        response = manageUser.manageSize(request)
        self.assertEqual(response, 'font-size-pequena')
        print("Test manageSize_small")

    def test_manageSize_large(self):
        request = RequestFactory().get('/')
        request.session = {'font_size': 'large'}
        response = manageUser.manageSize(request)
        self.assertEqual(response, 'font-size-grande')
        print("Test manageSize_large")

    def test_manageSize_default(self):
        request = RequestFactory().get('/')
        request.session = {'font_size': 'TEST'}
        response = manageUser.manageSize(request)
        self.assertEqual(response, manageUser.DEFAULT_FONT_SIZE)
        print("Test manageSize_default")

    def test_manageFamily_courier(self):
        request = RequestFactory().get('/')
        request.session = {'font_family': 'Courier New'}
        response = manageUser.manageFamily(request)
        self.assertEqual(response, 'font-family-courier')
        print("Test manageFamily_courier")

    def test_manageFamily_verdana(self):
        request = RequestFactory().get('/')
        request.session = {'font_family': 'Verdana'}
        response = manageUser.manageFamily(request)
        self.assertEqual(response, 'font-family-verdana')
        print("Test manageFamily_verdana")

    def test_manageFamily_times(self):
        request = RequestFactory().get('/')
        request.session = {'font_family': 'Times New Roman'}
        response = manageUser.manageFamily(request)
        self.assertEqual(response, 'font-family-times')
        print("Test manageFamily_times")

    def test_manageFamily_helvetica(self):
        request = RequestFactory().get('/')
        request.session = {'font_family': 'Helvetica'}
        response = manageUser.manageFamily(request)
        self.assertEqual(response, 'font-family-helvetica')
        print("Test manageFamily_helvetica")

    def test_manageFamily_arial(self):
        request = RequestFactory().get('/')
        request.session = {'font_family': 'Arial'}
        response = manageUser.manageFamily(request)
        self.assertEqual(response, 'font-family-arial')
        print("Test manageFamily_arial")

    def test_manageFamily_c4type(self):
        request = RequestFactory().get('/')
        request.session = {'font_family': 'C4 Type'}
        response = manageUser.manageFamily(request)
        self.assertEqual(response, 'font-family-c4type')
        print("Test manageFamily_c4type")

    def test_manageFamily_default(self):
        request = RequestFactory().get('/')
        request.session = {'font_family': 'TEST'}
        response = manageUser.manageFamily(request)
        self.assertEqual(response, manageUser.DEFAULT_FONT_FAMILY)
        print("Test manageFamily_default")

    def test_get_user_config(self):
        request = RequestFactory().get('/')
        request.session = {
            'username': 'TEST',
            'font_size': 'small',
            'font_family': 'Courier New'}
        response = manageUser.get_user_config(request)
        self.assertEqual(
            response,
            ('TEST',
             'font-size-pequena',
             'font-family-courier'))
        print("Test get_user_config")


class TestManageOrder(TestCase):

    def test_order_cameras_by_comments_(self):
        # Primero en orden ascendente
        response = manageOrder.order_cameras_by_comments('asc')
        self.assertEqual(response.query.order_by, ('num_comments',))
        print("Test order_cameras_by_comments_")

        # Ahora en orden descendente
        response = manageOrder.order_cameras_by_comments('desc')
        self.assertEqual(response.query.order_by, ('-num_comments',))
        print("Test order_cameras_by_comments_")

    def test_order_cameras_by_time(self):
        # Primero en orden ascendente
        response = manageOrder.order_cameras_by_time('asc')
        self.assertEqual(response.query.order_by, ('date',))
        print("Test order_cameras_by_time")

        # Ahora en orden descendente
        response = manageOrder.order_cameras_by_time('desc')
        self.assertEqual(response.query.order_by, ('-date',))
        print("Test order_cameras_by_time")

    def test_order_comments_by_time(self):
        # Creamos un comentario con fecha 2024-04-06
        comment = Comment.objects.create(name='TEST', camera=Camera.objects.create(source_id='TEST', id='TEST',
                                                                                   src='https://infocar.dgt.es/etraffic/data/camaras/4.jpg', name='TEST',
                                                                                   coordinates='TEST', img_path='TEST'), comment='TEST-TEST', date='2024-04-06', img_path_comment='TEST')
        # Guardamos el comentario
        comment.save()

        # Primero en orden ascendente
        response = manageOrder.order_comments_by_time(
            Comment.objects.all(), 'asc')
        self.assertEqual(response.query.order_by, ('date',))
        print("Test order_comments_by_time")

        # Ahora en orden descendente
        response = manageOrder.order_comments_by_time(
            Comment.objects.all(), 'desc')
        self.assertEqual(response.query.order_by, ('-date',))
        print("Test order_comments_by_time")

        # Borramos el comentario
        comment.delete()
