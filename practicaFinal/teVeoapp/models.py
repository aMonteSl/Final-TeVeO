from django.db import models
# Importar pillow para poder trabajar con imágenes
from PIL import Image

# Create your models here.

class Camera(models.Model):
    # Fuente de datos que proviene
    source_id = models.CharField(max_length=100)
    # Id de la camara, conseguido en el XML, puede ser una cadena de texto o un numero
    id = models.CharField(max_length=100, primary_key=True)
    # Primary_key es para que no se repitan las camaras, ya que el id es único, si se repite, salta la excepción de IntegrityError
    # src es la dirección https de la camara a la cual le pedimos la imagen
    src = models.CharField(max_length=200)
    # Nombre de la camara
    name = models.CharField(max_length=100)
    # Coordenadas de la camara
    coordinates = models.CharField(max_length=100)
    # Directorio donde se guardan las imagenes
    img_path = models.CharField(max_length=200)


    def __str__(self):
        return f'{self.source_id}{self.id} - {self.name}'

class Comment(models.Model):
    # Comentario de la camara
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    # Comentario, con blanck=False, no se puede dejar vacio
    comment = models.CharField(max_length=200, blank=False)
    # Fecha del comentario
    date = models.DateTimeField(auto_now_add=True)
    # Imagen de la cámara en el momento del comentario
    img_path_comment = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.camera} - {self.comment} - {self.date}'