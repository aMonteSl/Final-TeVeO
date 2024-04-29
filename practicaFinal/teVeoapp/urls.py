from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('comment/', views.comment_view, name='comment'),
    path('cameras/', views.mainCameras, name='mainCameras'),
    path('cameras/<str:id>/', views.camera),
    path('cameras/<str:id>/dyn', views.camera_dyn, name='camera_dyn'),
    path('cameras/<str:id>/img', views.latest_image, name='latest_image'),
    path('cameras/<str:id>/comment', views.get_comments, name='get_comments'),
]