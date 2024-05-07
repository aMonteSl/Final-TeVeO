# En forms.py
from django import forms  # Importas el módulo de formularios de Django

# Defines una clase para tu formulario que hereda de forms.Form


class ConfigForm(forms.Form):
    # Defines un campo de texto para el nombre de usuario.
    # El argumento label establece la etiqueta del campo
    # que se mostrará en el formulario.
    # max_length establece la longitud máxima
    # permitida para el texto ingresado.
    # required=False significa que este campo no es obligatorio.
    # Si el usuario no introduce nada, se enviará None.
    username = forms.CharField(
        label='Nombre de Usuario', max_length=100, required=False)

    # Defines un campo de selección para el tamaño de la fuente.
    # El argumento choices establece las opciones disponibles. Cada opción es
    # una tupla donde el primer elemento es el valor que se enviará si se
    # selecciona la opción, y el segundo elemento es la etiqueta de la opción
    # que se mostrará en el formulario.
    font_size = forms.ChoiceField(
        choices=[('large', 'Grande'),
                 ('standard', 'Estándar'),
                 ('small', 'Pequeña')])

    # Defines un campo de selección para la familia de fuentes, de manera
    # similar al campo font_size.
    font_family = forms.ChoiceField(choices=[
        ('Roboto', 'Roboto'),
        ('Arial', 'Arial'),
        ('Times New Roman', 'Times New Roman'),
        ('Verdana', 'Verdana'),
        ('Helvetica', 'Helvetica'),
        ('Courier New', 'Courier New'),
        ('C4 Type', 'C4 Type')
    ])
