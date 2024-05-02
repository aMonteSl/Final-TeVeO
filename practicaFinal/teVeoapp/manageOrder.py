from .models import Camera, Comment
from django.db.models import Count

def order_cameras_by_comments(order):
    order_field = 'num_comments' if order == 'asc' else '-num_comments'
    return Camera.objects.annotate(num_comments=Count('comment')).order_by(order_field)

def order_cameras_by_time(order):
    order_field = 'date' if order == 'asc' else '-date'
    return Comment.objects.order_by(order_field)

def order_comments_by_time(comments, order):
    order_field = 'date' if order == 'asc' else '-date'
    return comments.order_by(order_field)
