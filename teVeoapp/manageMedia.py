import os
import re
import requests
import random
import xml.dom.minidom
from urllib.request import urlopen
from .models import Camera

# Definir los identificadores de las fuentes de datos
SOURCE_ID_LIS1 = 'LIS1-'
SOURCE_ID_LIS2 = 'LIS2-'
SOURCE_ID_CCTV = 'CCTV-'
SOURCE_ID_DGT = 'DGT-'

# Definir las URLs como constantes globales
URL_LISTADO1 = ('https://gitlab.eif.urjc.es/cursosweb/2023-2024/'
                'final-teveo/-/raw/main/listado1.xml')
URL_LISTADO2 = ('https://gitlab.eif.urjc.es/cursosweb/2023-2024/'
                'final-teveo/-/raw/main/listado2.xml')
URL_CCTV = ('http://datos.madrid.es/egob/catalogo/202088-0-trafico-'
            'camaras.kml')
URL_DGT = ('https://infocar.dgt.es/datex2/dgt/CCTVSiteTablePublication/'
           'all/content.xml')


# Nombre de los archivos XML o KML
LIST1 = 'listado1.xml'
LIST2 = 'listado2.xml'
CCTV = 'CCTV.kml'
DGT = 'dgt.xml'


def get_xml_files():
    # Obtiene el directorio base del archivo actual
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Une el directorio base con la ruta específica 'teVeoapp/static/xml'
    directory = os.path.join(base_dir, 'teVeoapp/static/xml')
    # Crea una lista de todos los archivos en el directorio que terminan en
    # '.xml' o '.kml'
    result = [f for f in os.listdir(directory) if f.endswith(
        '.xml') or f.endswith('.kml')]
    # Invierte el orden de la lista
    result.reverse()
    return result


def load_cameras_from_xml1(camera):
    try:
        id = camera.getElementsByTagName('id')[0].firstChild.data
        src = camera.getElementsByTagName('src')[0].firstChild.data
        name = camera.getElementsByTagName('lugar')[0].firstChild.data
        coordinates = camera.getElementsByTagName('coordenadas')[
            0].firstChild.data
        # A las coordenadas les tengo que dar la vuelta, vienen al reves
        coordinates = ','.join(coordinates.split(',')[::-1])
        source_id = SOURCE_ID_LIS1
        return source_id, id, src, name, coordinates
    except IndexError:
        print("Error: No se pudo obtener uno o más elementos del archivo XML.")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None


def load_cameras_from_xml2(camera):
    try:
        # Obtiene el atributo 'id' del elemento 'camera'
        id = camera.getAttribute('id')
        # Obtiene el contenido del primer elemento 'url' dentro del elemento
        # 'camera'
        src = camera.getElementsByTagName('url')[0].firstChild.data
        # Obtiene el contenido del primer elemento 'info' dentro del elemento
        # 'camera'
        name = camera.getElementsByTagName('info')[0].firstChild.data
        # Obtiene el contenido del primer elemento 'latitude' dentro del
        # elemento 'camera'
        latitude = camera.getElementsByTagName('latitude')[0].firstChild.data
        # Obtiene el contenido del primer elemento 'longitude' dentro del
        # elemento 'camera'
        longitude = camera.getElementsByTagName(
            'longitude')[0].firstChild.data
        # Combina la latitud y la longitud en una cadena, separada por una
        # coma
        coordinates = f'{latitude},{longitude}'
        # Define el id de la fuente
        source_id = SOURCE_ID_LIS2
        # Devuelve los datos extraídos
    except IndexError:
        print("Error: No se pudo obtener uno o más elementos del archivo XML.")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
    return source_id, id, src, name, coordinates


def load_cameras_from_cctv(cameras):
    for placemark in cameras:
        try:
            # Obtener el número, nombre y descripción
            number = placemark.getElementsByTagName(
                'Data')[0].getElementsByTagName('Value')[0].firstChild.data
            name = placemark.getElementsByTagName(
                'Data')[1].getElementsByTagName('Value')[
                0].firstChild.data
            description = placemark.getElementsByTagName(
                'description')[
                0].firstChild.data

            # La descripción contiene la URL de la imagen
            # de la cámara en un elemento img
            # Podemos extraer la URL utilizando una expresión regular
            img_url_match = re.search('src=(https://[^ ]+)', description)
            if img_url_match is None:
                print(
                    f"""No se pudo encontrar la URL
                    de la imagen para la cámara {number}""")
                continue
            img_url = img_url_match.group(1)

            # Obtener las coordenadas
            coordinates = placemark.getElementsByTagName(
                'Point')[0].getElementsByTagName(
                    'coordinates')[0].firstChild.data
            # Hay que invertir las coordenadas
            coordinates = ','.join(coordinates.split(',')[::-1])
            # Eliminar el primer elemento de las coordenadas
            coordinates = coordinates.split(',')[1]

            # Añadir la cámara a la base de datos si no existe
            if not Camera.objects.filter(id=number).exists():
                cam = Camera(source_id=SOURCE_ID_CCTV, id=number,
                             src=img_url, name=name, coordinates=coordinates)
                cam.save()
            else:
                print(
                    f'La cámara con id {number} ya existe en la base de datos')
        except Exception as e:
            print(f"Error al procesar la cámara {number}: {e}")


def load_cameras_from_dgt(camera):
    try:
        # Obtener el id de la cámara
        camera_id = camera.getAttribute('id')
        # Obtener el nombre de la cámara
        camera_name = camera.getElementsByTagName(
            '_0:cctvCameraIdentification')[0].firstChild.data
        # Obtener la URL de la imagen de la cámara
        image_url = camera.getElementsByTagName(
            '_0:urlLinkAddress')[0].firstChild.data
        # Obtener la latitud de la cámara
        latitude = camera.getElementsByTagName(
            '_0:latitude')[0].firstChild.data
        # Obtener la longitud de la cámara
        longitude = camera.getElementsByTagName(
            '_0:longitude')[0].firstChild.data
        # Definir el id de la fuente
        source_id = SOURCE_ID_DGT
        # Devolver los datos extraídos
        return (source_id, camera_id, image_url, camera_name,
                f'{latitude},{longitude}')

    except IndexError:
        print("Error: No se pudo obtener uno o más elementos del archivo XML.")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None


def download_xml_files(xml_file, file_path):
    # Determinar la URL correcta en función del nombre del archivo XML
    if xml_file == 'listado1.xml':
        url = URL_LISTADO1
    elif xml_file == 'listado2.xml':
        url = URL_LISTADO2
    elif xml_file == 'CCTV.kml':
        url = URL_CCTV
    elif xml_file == 'dgt.xml':
        url = URL_DGT

    # Realizar una solicitud GET a la URL
    response = requests.get(url)
    # Escribir el contenido de la respuesta en un archivo
    with open(file_path, 'wb') as f:
        f.write(response.content)

    # Imprimir un mensaje de éxito
    print(f"Successfully downloaded {xml_file} from {url}")


def create_and_save_camera(sourc_id, id, src, name, coordinates):
    """
    Crea una nueva cámara y la guarda en la base de datos
    si no existe ya una cámara con el mismo id.
    """
    if not Camera.objects.filter(id=id).exists():
        cam = Camera(source_id=sourc_id, id=id, src=src,
                     name=name, coordinates=coordinates)
        cam.save()
    else:
        print(f'The camera with id {id} already exists in the database.')


def load_cameras_from_xml(xml_file):
    """
    Descarga el archivo XML, lo parsea y carga las cámaras en la base de datos.
    """
    # Obtener el directorio del archivo XML
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(base_dir, 'teVeoapp/static/xml')
    file_path = os.path.join(directory, xml_file)

    # Descargar el archivo XML
    download_xml_files(xml_file, file_path)

    # Parsear el archivo XML
    dom = xml.dom.minidom.parse(file_path)
    root = dom.documentElement

    # Cargar las cámaras del archivo XML en la base de datos
    if xml_file == LIST1:
        cameras = root.getElementsByTagName('camara')
        for camera in cameras:
            sourc_id, id, src, name, coordinates = load_cameras_from_xml1(
                camera)
            create_and_save_camera(sourc_id, id, src, name, coordinates)
    elif xml_file == LIST2:
        cameras = root.getElementsByTagName('cam')
        for camera in cameras:
            sourc_id, id, src, name, coordinates = load_cameras_from_xml2(
                camera)
            create_and_save_camera(sourc_id, id, src, name, coordinates)
    elif xml_file == CCTV:
        cameras = root.getElementsByTagName('Placemark')
        load_cameras_from_cctv(cameras)
    elif xml_file == DGT:
        cameras = root.getElementsByTagName('_0:cctvCameraMetadataRecord')
        for camera in cameras:
            sourc_id, id, src, name, coordinates = load_cameras_from_dgt(
                camera)
            create_and_save_camera(sourc_id, id, src, name, coordinates)


def download_and_save_image(cam):
    """
    Descarga la imagen de la cámara y la guarda en el sistema de archivos.
    """
    try:
        print(f"Processing camera with id {cam.id}")
        print(f"URL for camera with id {cam.id}: {cam.src}")
        response = urlopen(cam.src)
        img = response.read()
        img_path = os.path.join('img/data', f'{cam.source_id}{cam.id}.jpg')
        full_img_path = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), 'teVeoapp/static', img_path)
        with open(full_img_path, 'wb') as f:
            f.write(img)
        cam.img_path = img_path
        cam.save()
        print(
            f"""Successfully saved image for
            camera with id {cam.id} and path {img_path}""")
    except Exception as e:
        print(f"Failed to process camera with id {cam.id}. Error: {str(e)}")


def get_img_of_cameras(xml_file):
    """
    Obtiene las cámaras del archivo XML especificado
      y descarga y guarda sus imágenes.
    """
    # Determinar el id de la fuente en función del nombre del archivo XML
    if xml_file == LIST1:
        cameras = Camera.objects.filter(source_id=SOURCE_ID_LIS1)
    elif xml_file == LIST2:
        cameras = Camera.objects.filter(source_id=SOURCE_ID_LIS2)
    elif xml_file == CCTV:
        cameras = Camera.objects.filter(source_id=SOURCE_ID_CCTV)
    elif xml_file == DGT:
        cameras = Camera.objects.filter(source_id=SOURCE_ID_DGT)

    # Descargar y guardar la imagen de cada cámara
    for cam in cameras:
        download_and_save_image(cam)


def get_actual_img(id):
    """
    Obtiene la imagen actual de la cámara con el id especificado.
    """
    # Obtener la cámara de la base de datos
    cam = Camera.objects.filter(id=id).first()
    if cam is None:
        print(f"No se encontró ninguna cámara con el id {id}")
        return None

    # Descargar y guardar la imagen de la cámara
    download_and_save_image(cam)

    return cam.img_path


def get_random_img():
    """
    Obtiene una imagen aleatoria del directorio de imágenes.
    """
    # Obtener el directorio de las imágenes
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(base_dir, 'teVeoapp/static/img/data')

    # Obtener la lista de archivos .jpg en el directorio
    result = [f for f in os.listdir(directory) if f.endswith('.jpg')]

    # Si hay al menos una imagen, seleccionar una aleatoriamente y devolverla
    if result:
        return random.choice(result)

    # Si no hay imágenes, devolver None
    return None


def delete_files_in_directory(directory):
    """
    Elimina todos los archivos en el directorio especificado.
    """
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))


def clear_all():
    """
    Elimina todas las cámaras y todas las imágenes.
    """
    # Eliminar todas las cámaras
    Camera.objects.all().delete()
    print("All cameras deleted")

    # Obtener el directorio base
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Eliminar todas las imágenes en el directorio de datos
    data_directory = os.path.join(base_dir, 'teVeoapp/static/img/data')
    delete_files_in_directory(data_directory)

    # Eliminar todas las imágenes en el directorio de comentarios
    comments_directory = os.path.join(
        base_dir, 'teVeoapp/static/img/comments')
    delete_files_in_directory(comments_directory)

    print("All images deleted")


def save_img_comment(path):
    """
    Copia la imagen del path a la carpeta static/img/comments.
    La copia tendrá como nombre el nombre de la imagen original
      con un sufijo que sea el número de comentario de dicha imagen.
    """
    try:
        # Obtener el directorio base y el directorio de comentarios
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))
        directory = os.path.join(base_dir, 'teVeoapp/static/img/comments')

        # Obtener la lista de archivos .jpg en el directorio de comentarios
        result = [f for f in os.listdir(directory) if f.endswith('.jpg')]

        # Crear el nuevo path para la imagen
        new_path = os.path.join(
            'img/comments', f'{len(result)}_{os.path.basename(path)}')
        full_path = os.path.join(base_dir, 'teVeoapp/static', new_path)

        # Copiar la imagen al nuevo path
        with open(full_path, 'wb') as f:
            image_path = os.path.join(base_dir, 'teVeoapp/static', path)
            with open(image_path, 'rb') as f2:
                f.write(f2.read())

        return new_path
    except Exception as e:
        print(f"Failed to save image comment. Error: {str(e)}")
        return None
