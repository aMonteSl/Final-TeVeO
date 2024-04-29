import os
import xml.dom.minidom
from random import randint
from urllib.request import urlopen
from .models import Camera

def get_xml_files():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(base_dir, 'teVeoapp/static/xml')
    result = [f for f in os.listdir(directory) if f.endswith('.xml')]
    # Dar la vuelta al orden de result
    result = result[::-1]
    return result

def load_cameras_from_xml1(camera):
    
    id = camera.getElementsByTagName('id')[0].firstChild.data
    src = camera.getElementsByTagName('src')[0].firstChild.data
    name = camera.getElementsByTagName('lugar')[0].firstChild.data
    coordinates = camera.getElementsByTagName('coordenadas')[0].firstChild.data
    # A las coordenadas les tengo que dar la vuelta, vienen al reves
    coordinates = ','.join(coordinates.split(',')[::-1])
    source_id = 'LIS1-'
    return source_id, id, src, name, coordinates

def load_cameras_from_xml2(camera):
    id = camera.getAttribute('id')
    src = camera.getElementsByTagName('url')[0].firstChild.data
    name = camera.getElementsByTagName('info')[0].firstChild.data
    latitude = camera.getElementsByTagName('latitude')[0].firstChild.data
    longitude = camera.getElementsByTagName('longitude')[0].firstChild.data
    coordinates = f'{latitude},{longitude}'
    source_id = 'LIS2-'
    return source_id, id, src, name, coordinates

def load_cameras_from_xml(xml_file):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(base_dir, 'teVeoapp/static/xml')
    file_path = os.path.join(directory, xml_file)
    dom = xml.dom.minidom.parse(file_path)
    root = dom.documentElement
    if xml_file == 'listado1.xml':
        cameras = root.getElementsByTagName('camara')
        for camera in cameras:
            sourc_id, id, src, name, coordinates = load_cameras_from_xml1(camera)
            if not Camera.objects.filter(id=id).exists():
                cam = Camera(source_id= sourc_id, id=id, src=src, name=name, coordinates=coordinates)
                cam.save()
            else:
                print(f'La cámara con id {id} ya existe en la base de datos')
    elif xml_file == 'listado2.xml':
        print('listado2.xml')
        cameras = root.getElementsByTagName('cam')
        for camera in cameras:
            sourc_id, id, src, name, coordinates = load_cameras_from_xml2(camera)
            if not Camera.objects.filter(id=id).exists():
                cam = Camera(source_id= sourc_id, id=id, src=src, name=name, coordinates=coordinates)
                cam.save()
            else:
                print(f'La cámara con id {id} ya existe en la base de datos')



def get_img_of_cameras():
    cameras = Camera.objects.all()
    for cam in cameras:
        try:
            print(f"Processing camera with id {cam.id}")
            print(f"URL for camera with id {cam.id}: {cam.src}")
            response = urlopen(cam.src)
            img = response.read()
            #print(f"First 64 bytes of image data: {img[:4000]}")  # Add this line
            img_path = os.path.join('img/data', f'{cam.source_id}{cam.id}.jpg')
            full_img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'teVeoapp/static', img_path)
            with open(full_img_path, 'wb') as f:
                f.write(img)
            cam.img_path = img_path
            cam.save()
            print(f"Successfully saved image for camera with id {cam.id} and path {img_path}")
        except Exception as e:
            print(f"Failed to process camera with id {cam.id}. Error: {str(e)}")

def get_actual_img(id):
    # Obtener la imagen actual de la camara
    cam = Camera.objects.filter(id=id).first()
    try:
        response = urlopen(cam.src)
        img = response.read()
        img_path = os.path.join('img/data', f'{cam.source_id}{cam.id}.jpg')
        full_img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'teVeoapp/static', img_path)
        # Borro la imagen anterior
        if cam.img_path:
            os.remove(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'teVeoapp/static', cam.img_path))
        
        with open(full_img_path, 'wb') as f:
            f.write(img)
        cam.img_path = img_path
        cam.save()
        print(f"Successfully saved image for camera with id {cam.id} and path {img_path}")
        return img_path
    except Exception as e:
        print(f"Failed to process camera with id {cam.id}. Error: {str(e)}")
        return None


def get_random_img():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(base_dir, 'teVeoapp/static/img/data')
    result = [f for f in os.listdir(directory) if f.endswith('.jpg')]
    # Tengo que escoger una imagen aleatoria
    if len(result) > 0:
        random_index = randint(0, len(result) - 1)
        return result[random_index]
    else:
        return None
    
def clear_all():
    Camera.objects.all().delete()
    print("All cameras deleted")
    # Tambien borro las imagenes
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(base_dir, 'teVeoapp/static/img/data')
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))
    print("All images deleted")
