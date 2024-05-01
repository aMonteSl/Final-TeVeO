# En forms.py
from django import forms

class ConfigForm(forms.Form):
    username = forms.CharField(label='Nombre de Usuario', max_length=100, required=False) # required=False para que no sea obligatorio y despueś poner Anonimo
    font_size = forms.ChoiceField(choices=[('large', 'Grande'), ('standard', 'Estándar'), ('small', 'Pequeña')])
    font_family = forms.ChoiceField(choices=[('Roboto', 'Roboto'), ('Arial', 'Arial'), ('Times New Roman', 'Times New Roman'), ('Verdana', 'Verdana'), ('Helvetica', 'Helvetica'), ('Courier New', 'Courier New')])