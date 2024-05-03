from django.test import TestCase, RequestFactory
# RequestFactory se usa para crear request falsos
from . import manageUser
from . import manageOrder
from .models import Camera, Comment
from . import views


class ManageUserTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_manageNameLogin(self):
        request = self.factory.get('/')
        request.session = {'username': 'TestUser'}
        self.assertEqual(manageUser.manageNameLogin(request), 'TestUser')

        request.session = {'username': ''}
        self.assertEqual(
            manageUser.manageNameLogin(request),
            manageUser.DEFAULT_NAME)

        request.session = {}
        self.assertEqual(
            manageUser.manageNameLogin(request),
            manageUser.DEFAULT_NAME)

    def test_manageSize(self):
        request = self.factory.get('/')
        request.session = {'font_size': 'small'}
        self.assertEqual(manageUser.manageSize(request), 'font-size-pequena')

        request.session = {'font_size': 'large'}
        self.assertEqual(manageUser.manageSize(request), 'font-size-grande')

        request.session = {'font_size': 'medium'}
        self.assertEqual(
            manageUser.manageSize(request),
            manageUser.DEFAULT_FONT_SIZE)

        request.session = {}
        self.assertEqual(
            manageUser.manageSize(request),
            manageUser.DEFAULT_FONT_SIZE)

    def test_manageFamily(self):
        request = self.factory.get('/')
        request.session = {'font_family': 'Courier New'}
        self.assertEqual(
            manageUser.manageFamily(request),
            'font-family-courier')

        request.session = {'font_family': 'Verdana'}
        self.assertEqual(
            manageUser.manageFamily(request),
            'font-family-verdana')

        request.session = {'font_family': 'Times New Roman'}
        self.assertEqual(
            manageUser.manageFamily(request),
            'font-family-times')

        request.session = {'font_family': 'Helvetica'}
        self.assertEqual(
            manageUser.manageFamily(request),
            'font-family-helvetica')

        request.session = {'font_family': 'Arial'}
        self.assertEqual(
            manageUser.manageFamily(request),
            'font-family-arial')

        request.session = {'font_family': 'C4 Type'}
        self.assertEqual(
            manageUser.manageFamily(request),
            'font-family-c4type')

        request.session = {'font_family': 'Roboto'}
        self.assertEqual(
            manageUser.manageFamily(request),
            manageUser.DEFAULT_FONT_FAMILY)

        request.session = {}
        self.assertEqual(
            manageUser.manageFamily(request),
            manageUser.DEFAULT_FONT_FAMILY)

    def test_get_user_config(self):
        request = self.factory.get('/')
        request.session = {
            'username': 'TestUser',
            'font_size': 'small',
            'font_family': 'Courier New'}
        self.assertEqual(
            manageUser.get_user_config(request),
            ('TestUser',
             'font-size-pequena',
             'font-family-courier'))


class ManageOrderTest(TestCase):
    def setUp(self):
        self.camera1 = Camera.objects.create(
            source_id='1', src='src1', img_path='path1')
        self.camera2 = Camera.objects.create(
            source_id='2', src='src2', img_path='path2')
        self.comment1 = Comment.objects.create(
            camera=self.camera1, text='comment1')
        self.comment2 = Comment.objects.create(
            camera=self.camera1, text='comment2')
        self.comment3 = Comment.objects.create(
            camera=self.camera2, text='comment3')

    def test_order_cameras_by_comments(self):
        cameras = manageOrder.order_cameras_by_comments('asc')
        self.assertEqual(cameras[0], self.camera2)
        self.assertEqual(cameras[1], self.camera1)

        cameras = manageOrder.order_cameras_by_comments('desc')
        self.assertEqual(cameras[0], self.camera1)
        self.assertEqual(cameras[1], self.camera2)

    def test_order_cameras_by_time(self):
        cameras = manageOrder.order_cameras_by_time('asc')
        self.assertEqual(cameras[0], self.camera1)
        self.assertEqual(cameras[1], self.camera2)

        cameras = manageOrder.order_cameras_by_time('desc')
        self.assertEqual(cameras[0], self.camera2)
        self.assertEqual(cameras[1], self.camera1)

    def test_order_comments_by_time(self):
        comments = Comment.objects.all()
        ordered_comments = manageOrder.order_comments_by_time(comments, 'asc')
        self.assertEqual(ordered_comments[0], self.comment1)
        self.assertEqual(ordered_comments[1], self.comment2)
        self.assertEqual(ordered_comments[2], self.comment3)

        ordered_comments = manageOrder.order_comments_by_time(
            comments, 'desc')
        self.assertEqual(ordered_comments[0], self.comment3)
        self.assertEqual(ordered_comments[1], self.comment2)
        self.assertEqual(ordered_comments[2], self.comment1)
