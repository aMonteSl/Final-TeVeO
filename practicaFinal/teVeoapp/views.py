from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from .models import Camera, Comment
from django.utils import timezone
from .manageXML import get_xml_files, load_cameras_from_xml, get_img_of_cameras, get_random_img, clear_all, get_actual_img, save_img_comment
from .manageUser import get_user_config
from django.db.models import Count
import time
from .forms import ConfigForm

# Create your views here.

SELECTED_XML = "selected_xml"


def config(request):
    if request.method == 'POST':
        #print("Recibiendo datos del formulario")
        form = ConfigForm(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            request.session['font_size'] = form.cleaned_data['font_size']
            request.session['font_family'] = form.cleaned_data['font_family']
            #print("Redirigiendo a la página principal")
            return HttpResponseRedirect('/')
        else:
            print(form.errors)
    else:
        form = ConfigForm()
    #print("Mostrando la página de configuración")
    #print(f"{request.method}")
    return render(request, 'config.html', {'form': form})


@csrf_exempt
def index(request):
    # Devolver la plantilla index.html
    template = loader.get_template('index.html')
    # Asi puedo pasar los comentarios ordenados por fecha
    order = request.POST.get('order', 'desc')
    if request.method == 'POST':
        if order == 'asc':
            comments = Comment.objects.order_by('date')
        else:
            comments = Comment.objects.order_by('-date')
        
    else:
        comments = Comment.objects.order_by('-date')
    
    # Manejo de la sesion del usuario
    username, font_size, font_family = get_user_config(request)
    print(f"Username: {username}, Font size: {font_size}, Font family: {font_family}")
    

    context = {
        'comments': comments,
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
    }
    
    return HttpResponse(template.render(context))
    

@csrf_exempt
def mainCameras(request):
    # Un listado de las fuentes de datos disponibles, con un botón junto a cada
    # una de ellas. Si se pulsa el botón se descargará esa fuente de datos, y
    # se almacenará la información correspondiente en la base de datos (solo
    # las cámaras que tenga un identificador diferente a los ya almacenados
    # para esa fuente de datos).
    # Un listado de todas las cámaras, opcionalmente paginado. En la parte
    # superior aparecerá la imagen de una cámara aleatoria. Debajo, para
    # cada cámara, se verá su identificador, junto a dos enlaces: uno a la
    # página de la cámara, otro a la página dinámica de la cámara. Además,
    # aparecerá el nombre de la cámara, y el número de comentarios que tiene.
    # Las cámaras aparecerán ordenadas por número de comentarios (de más
    # a menos comentarios).

    # Primero debo de obtener las fuentes de datos disponibles en static/xml
    random_img = None
    # Ordenar las camaras por el número de comentarios de mas a menos comentarios
    cameras = Camera.objects.annotate(num_comments=Count('comment')).order_by('-num_comments')
    if request.method == 'POST':
        xml_selected = request.POST.get(f'{SELECTED_XML}')
        order = request.POST.get('order', 'desc')
        if order == 'asc':
            cameras = Camera.objects.annotate(num_comments=Count('comment')).order_by('num_comments')
        else:
            cameras = Camera.objects.annotate(num_comments=Count('comment')).order_by('-num_comments')
        if xml_selected == "clean":
            clear_all()
        elif xml_selected is not None:
            load_cameras_from_xml(xml_selected)
            get_img_of_cameras()

    random_img = get_random_img()
    xml_files = get_xml_files()
    template = loader.get_template('mainCameras.html')
    context = {
        'request': request,
        'xml_files': xml_files,
        'random_img': random_img,
        'cameras': cameras,
        'cameras_count': cameras.count(),
        'comments_count': Comment.objects.count(),
    }
    return HttpResponse(template.render(context))



@csrf_exempt
def camera(request, id):
    # Seleccionar la cámara con el identificador indicado. Si no existe, se
    # mostrará un mensaje de error. En caso contrario, se mostrará la imagen
    # de la cámara, y un enlace para volver al listado de cámaras.
    camera = Camera.objects.filter(id=id).first()
    # Obtener todos los comentarios de la camera por defecto de más reciente a más antiguo
    comments = Comment.objects.filter(camera=camera).order_by('-date')
    
    if camera is None:
        return HttpResponse("Cámara no encontrada")
    
    if request.method == 'POST':
        order = request.POST.get('order', 'desc')
        if order == 'asc':
            comments = Comment.objects.filter(camera=camera).order_by('date')
        else:
            comments = Comment.objects.filter(camera=camera).order_by('-date')

    template = loader.get_template('camera.html')
    context = {
        'request': request,
        'camera': camera,
        'comments': comments,
        'cameras_count': Camera.objects.count(),  
        'comments_count': Comment.objects.count(),

    }
    return HttpResponse(template.render(context))

@csrf_exempt
def comment_view(request):
    camera_id = request.GET.get('camera_id')
    camera = Camera.objects.filter(id=camera_id).first()

    if camera is None:
        return HttpResponse("Cámara no encontrada")

    if request.method == 'POST':
        comment_text = request.POST.get('body')  # Cambiar 'cuerpo' a 'body'
        if comment_text:  # Verificar si comment_text no es vacío
            # Guardar el comentario en la base de datos con la camara, comentario, fecha y la imagen de la cámara en ese momento
            img_comment = save_img_comment(camera.img_path)
            print(f"Este es el path de la imagen del comentario: {img_comment}")
            comment = Comment(camera=camera, comment=comment_text, date=timezone.now() ,img_path_comment=img_comment)
            comment.save()


    comments = Comment.objects.filter(camera=camera)
    print("Estos son los comentarios: ")
    for comment in comments:
        print(comment.comment)
    context = {
        'request': request,
        'comments': comments,
        'camera': camera,
        'now': timezone.now(),
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
    }
    return render(request, 'comment.html', context)


@csrf_exempt
def camera_dyn(request, id):
    # Seleccionar la cámara con el identificador indicado. Si no existe, se
    # mostrará un mensaje de error. En caso contrario, se mostrará la imagen
    # de la cámara, y un enlace para volver al listado de cámaras.
    template = loader.get_template('camera_dyn.html')
    camera = Camera.objects.filter(id=id).first()
    camera.img_path = get_actual_img(id)
    if camera is None:
        return HttpResponse("Cámara no encontrada")
    if request.method == 'POST':
        comment_text = request.POST.get('body')  # Cambiar 'cuerpo' a 'body'
        if comment_text:  # Verificar si comment_text no es vacío
            # Guardar el comentario en la base de datos con la camara, comentario, fecha y la imagen de la cámara en ese momento
            img_comment = save_img_comment(camera.img_path)
            print(f"Este es el path de la imagen del comentario: {img_comment}")
            comment = Comment(camera=camera, comment=comment_text, date=timezone.now() ,img_path_comment=img_comment)
            comment.save()
    # Obtener todos los comentarios de la camera de más reciente a más antiguo
    comments = Comment.objects.filter(camera=camera).order_by('-date')
    context = {
        'request': request,
        'comments': comments,
        'camera': camera,
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
        'now': timezone.now(),
    }
    return HttpResponse(template.render(context))

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
        'latest_image_url': img_path + '?t=' + str(time.time()),
    }
    return render(request, 'image.html', context)
    
def get_comments(request, id):
    camera = Camera.objects.filter(id=id).first()
    if camera is None:
        return HttpResponse("Cámara no encontrada")
    # Obtener todos los comentarios de la camera de más reciente a más antiguo
    comments = Comment.objects.filter(camera=camera).order_by('-date')
    print("Estos son los comentarios: ")
    for comment in comments:
        print(comment.comment)
    context = {
        'request': request,
        'comments': comments,
        'camera': camera,
        'now': timezone.now(),
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
    }
    return render(request, 'get_comments.html', context)
