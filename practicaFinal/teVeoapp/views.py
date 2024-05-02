from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from .models import Camera, Comment
from django.utils import timezone
from .manageMedia import * # Importar todas las funciones de media_operations
from .manageUser import get_user_config
from .manageOrder import * # Importar todas las funciones de manageOrder
from django.db.models import Count
import time
from .forms import ConfigForm
from urllib.parse import urlparse
from importlib import import_module
from django.conf import settings
from django.contrib import messages

# Create your views here.

SELECTED_XML = "selected_xml"

def set_session(request):
    """
    Establece la sesión actual en la sesión con el identificador de sesión en el enlace de autorización.
    """
    if request.method == 'POST':
        auth_link = request.POST.get('auth_link')
        session_key = urlparse(auth_link).query
        engine = import_module(settings.SESSION_ENGINE)
        session = engine.SessionStore(session_key)
        if session.exists(session.session_key):
            request.session = session
        else:
            messages.error(request, 'El enlace de autorización no es válido.')
    return redirect('index')

def config(request):
    # If es un post request, se obtienen los datos del formulario y se guardan en la sesion
    if request.method == 'POST':
        #print("Recibiendo datos del formulario")
        # Se crea un objeto de tipo ConfigForm con los datos del formulario
        form = ConfigForm(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            request.session['font_size'] = form.cleaned_data['font_size']
            request.session['font_family'] = form.cleaned_data['font_family']
            #print("Redirigiendo a la página principal")
            # Redirigir a la página principal
            return HttpResponseRedirect('/')
        else:
            # Si el formulario no es válido, se muestran los errores en la consola
            print(form.errors)
    else:
        # Si no es un post request, se crea un formulario vacio
        form = ConfigForm()
    #print("Mostrando la página de configuración")
    #print(f"{request.method}")
    # En caso de que no sea un post request, o no sea valido, se muestra la página de configuración
    return render(request, 'config.html', {'form': form})


def index(request):
    # Manejo de la sesion del usuario
    username, font_size, font_family = get_user_config(request)

    # Odenar los comentario por tiempo
    order = 'desc'
    if request.method == 'POST':
        order = request.POST.get('order', 'desc')

    comments = order_cameras_by_time(order)
    
    # Crear el contexto
    context = {
        'comments': comments,
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
        'username': username,
        'font_size': font_size,
        'font_family': font_family,
    }
    
    # Importante hacer con render y no con HttpResponse porque render es mas seguro y maneja mejor los errores
    return render(request, 'index.html', context)
    

def mainCameras(request):
    # Obtener las fuentes de datos disponibles en static/xml
    random_img = None
    order = 'desc'
    if request.method == 'POST':
        xml_selected = request.POST.get(f'{SELECTED_XML}')
        order = request.POST.get('order', 'desc')
        if xml_selected == "clean":
            clear_all()
        elif xml_selected is not None:
            print(f"XML seleccionado: {xml_selected}")
            load_cameras_from_xml(xml_selected)
            get_img_of_cameras(xml_selected)

    cameras = order_cameras_by_comments(order)
    
    username, font_size, font_family = get_user_config(request)
    #print(f"Username en mainCameras: {username}, Font size: {font_size}, Font family: {font_family}")

    random_img = get_random_img()
    xml_files = get_xml_files()

    context = {
        'request': request,
        'xml_files': xml_files,
        'random_img': random_img,
        'cameras': cameras,
        'cameras_count': cameras.count(),
        'comments_count': Comment.objects.count(),
        'username': username,
        'font_size': font_size,
        'font_family': font_family,
    }
    return render(request, 'mainCameras.html', context)


def camera(request, id):
    # Seleccionar la cámara con el identificador indicado. Si no existe, se
    # mostrará un mensaje de error. En caso contrario, se mostrará la imagen
    # de la cámara, y un enlace para volver al listado de cámaras.

    # Obtener la cámara con el id indicado
    camera = Camera.objects.filter(id=id).first()
    
    if camera is None:
        return HttpResponse("Cámara no encontrada")

    # Ordenar los comentarios por tiempo
    order = 'desc'
    if request.method == 'POST':
        order = request.POST.get('order', 'desc')

    # Obtener todos los comentarios de la camera ordenados por fecha
    comments = order_comments_by_time(Comment.objects.filter(camera=camera), order)
    
    # Obtener el nombre de usuario, tamaño de fuente y familia de fuentes
    username, font_size, font_family = get_user_config(request)

    context = {
        'request': request,
        'camera': camera,
        'comments': comments,
        'cameras_count': Camera.objects.count(),  
        'comments_count': Comment.objects.count(),
        'username': username,
        'font_size': font_size,
        'font_family': font_family,
    }

    return render(request, 'camera.html', context)

# Funcion para guardar un comentario si se ha hecho un post request
def save_comment_if_post(request, camera, name):
    comment_text = request.POST.get('body')  # Cambiar 'cuerpo' a 'body'
    if comment_text:  # Verificar si comment_text no es vacío
        # Guardar el comentario en la base de datos con la camara, comentario, fecha y la imagen de la cámara en ese momento
        img_comment = save_img_comment(camera.img_path)
        comment = Comment(name=name, camera=camera, comment=comment_text, date=timezone.now() ,img_path_comment=img_comment)
        comment.save()


def comment_view(request):
    camera_id = request.GET.get('camera_id')
    camera = Camera.objects.filter(id=camera_id).first()
    username, font_size, font_family = get_user_config(request)

    if camera is None:
        return HttpResponse("Cámara no encontrada")
    
    if request.method == 'POST':
        save_comment_if_post(request, camera, username)

    

    # Obtener todos los comentarios de la camera de más reciente a más antiguo
    comments = Comment.objects.filter(camera=camera).order_by('-date')
    context = {
        'request': request,
        'comments': comments,
        'camera': camera,
        'now': timezone.now(),
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
        'username': username,
        'font_size': font_size,
        'font_family': font_family,
    }
    return render(request, 'comment.html', context)


def camera_dyn(request, id):
    # Seleccionar la cámara con el identificador indicado. Si no existe, se
    # mostrará un mensaje de error. En caso contrario, se mostrará la imagen
    # de la cámara, y un enlace para volver al listado de cámaras.
    camera = Camera.objects.filter(id=id).first()
    username, font_size, font_family = get_user_config(request)

    if camera is None:
        return HttpResponse("Cámara no encontrada")

    camera.img_path = get_actual_img(id)
    print(f"Imagen actual: {camera.img_path}")

    if request.method == 'POST':
        save_comment_if_post(request, camera, username)

    

    # Obtener todos los comentarios de la camera de más reciente a más antiguo
    comments = Comment.objects.filter(camera=camera).order_by('-date')
    context = {
        'request': request,
        'comments': comments,
        'camera': camera,
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
        'now': timezone.now(),
        'username': username,
        'font_size': font_size,
        'font_family': font_family,
    }
    return render(request, 'camera_dyn.html', context)

def get_latest_image_url(img_path):
    """
    Obtiene la URL de la última imagen, añadiendo un parámetro de tiempo para evitar el caché del navegador.
    """
    if img_path is None:
        print("No se encontró ninguna imagen")
        return None

    return img_path + '?t=' + str(time.time())

def latest_image(request, id):
    camera = Camera.objects.filter(id=id).first()
    if camera is None:
        return HttpResponse("Cámara no encontrada")

    img_path = get_actual_img(id)
    context = {
        'request': request,
        'camera': camera,
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
        'latest_image_url': get_latest_image_url(img_path),
    }
    return render(request, 'image.html', context)
    
def get_comments(request, id):
    camera = Camera.objects.filter(id=id).first()
    if camera is None:
        return HttpResponse("Cámara no encontrada")

    # Obtener todos los comentarios de la camera de más reciente a más antiguo
    comments = Comment.objects.filter(camera=camera).order_by('-date')

    context = {
        'request': request,
        'comments': comments,
        'camera': camera,
        'now': timezone.now(),
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
    }
    return render(request, 'get_comments.html', context)

def camera_json(id):
    """
    Devuelve los datos de la cámara especificada en formato JSON.
    """
    try:
        cam = Camera.objects.get(id=id)
    except Camera.DoesNotExist:
        raise Http404("Cámara no encontrada")
    
    # Obtener el número de comentarios de la cámara
    num_comments = Comment.objects.filter(camera=cam).count()

    data = {
        'id': cam.id,
        'source_id': cam.source_id,
        'src': cam.src,
        'img_path': cam.img_path,
        'num_comments': num_comments,  
    }
    return JsonResponse(data)

def cameras_json():
    """
    Devuelve los datos de todas las cámaras en formato JSON.
    """
    cameras = Camera.objects.all()
    data = []
    for cam in cameras:
        # Obtener el número de comentarios de la cámara
        num_comments = Comment.objects.filter(camera=cam).count()
        data.append({
            'id': cam.id,
            'source_id': cam.source_id,
            'src': cam.src,
            'img_path': cam.img_path,
            'num_comments': num_comments,
        })
    return JsonResponse(data, safe=False)

def generate_auth_link(request):
    """
    Genera un enlace de autorización para la sesión actual.
    """
    session_key = request.session.session_key
    if session_key is None:
        # Si no hay una sesión, crea una
        request.session.create()
        session_key = request.session.session_key
    auth_link = request.build_absolute_uri('/') + '?' + session_key
    return JsonResponse({'auth_link': auth_link})

def help(request):
    # Hacer pagina de ayuda
    return HttpResponse("Ayuda")


