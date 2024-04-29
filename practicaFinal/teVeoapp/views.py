from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from .models import Camera, Comment
from django.utils import timezone
from .manageXML import get_xml_files, load_cameras_from_xml, get_img_of_cameras, get_random_img, clear_all, get_actual_img
# Create your views here.

SELECTED_XML = "selected_xml"

@csrf_exempt
def index(request):
    # Devolver la plantilla index.html
    template = loader.get_template('index.html')
    return HttpResponse(template.render())



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
    list_cameras, random_img = None, None
    cameras = Camera.objects.all()
    if request.method == 'POST':
        xml_selected = request.POST.get(f'{SELECTED_XML}')
        if xml_selected == "clean":
            clear_all()
        else:
            load_cameras_from_xml(xml_selected)
            get_img_of_cameras()
            random_img = get_random_img()
            print("Random img: ", random_img)
            cameras = Camera.objects.all()

    xml_files = get_xml_files()
    template = loader.get_template('mainCameras.html')
    context = {
        'request': request,
        'xml_files': xml_files,
        'random_img': random_img,
        'cameras': cameras
    }
    return HttpResponse(template.render(context))



@csrf_exempt
def camera(request, id):
    # Seleccionar la cámara con el identificador indicado. Si no existe, se
    # mostrará un mensaje de error. En caso contrario, se mostrará la imagen
    # de la cámara, y un enlace para volver al listado de cámaras.
    camera = Camera.objects.filter(id=id).first()
    if camera is None:
        return HttpResponse("Cámara no encontrada")
    template = loader.get_template('camera.html')
    context = {
        'request': request,
        'camera': camera
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
            new_comment = Comment(comment=comment_text, camera=camera, date=timezone.now())
            new_comment.save()

    comments = Comment.objects.filter(camera=camera)
    print("Estos son los comentarios: ")
    for comment in comments:
        print(comment.comment)
    context = {
        'request': request,
        'comments': comments,
        'camera': camera,
        'now': timezone.now()
    }
    return render(request, 'comment.html', context)


# @csrf_exempt Se lo quito para poder hacer peticiones GET
def camera_dyn(request, id):
    # Seleccionar la cámara con el identificador indicado. Si no existe, se
    # mostrará un mensaje de error. En caso contrario, se mostrará la imagen
    # de la cámara, y un enlace para volver al listado de cámaras.
    template = loader.get_template('camera_dyn.html')
    camera = Camera.objects.filter(id=id).first()
    if camera is None:
        return HttpResponse("Cámara no encontrada")
    context = {
        'request': request,
        'camera': camera
    }
    return HttpResponse(template.render(context))

def latest_image(request, id):
    camera = Camera.objects.filter(id=id).first()
    if camera is None:
        return HttpResponse("Cámara no encontrada")
    img_path = get_actual_img(id)
    context = {
        'request': request,
        'camera': camera
    }
    return render(request, 'image.html', context)
    
def get_comments(request, id):
    camera = Camera.objects.filter(id=id).first()
    if camera is None:
        return HttpResponse("Cámara no encontrada")
    comments = Comment.objects.filter(camera=camera)
    print("Estos son los comentarios: ")
    for comment in comments:
        print(comment.comment)
    context = {
        'request': request,
        'comments': comments,
        'camera': camera,
        'now': timezone.now()
    }
    return render(request, 'comment.html', context)