from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('config/', views.config, name='config'),
    path('config/auth_link', views.generate_auth_link, name='auth_link'),
    path('config/set_session', views.set_session, name='set_session'),
    path('ayuda/', views.help, name='ayuda'),
    path('comentario/', views.comment_view, name='comment'),
    path('camaras/', views.mainCameras, name='mainCameras'),
    path('camaras/json', views.cameras_json, name='cameras_json'),
    path('camaras/<str:id>/', views.camera, name='camera'),
    path('camaras/<str:id>/json', views.camera_json, name='camera_json'),
    path('camaras/<str:id>/dyn', views.camera_dyn, name='camera_dyn'),
    path('camaras/<str:id>/img', views.latest_image, name='latest_image'),
    path('camaras/<str:id>/comment', views.get_comments, name='get_comments'),
]
