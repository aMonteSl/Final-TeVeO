# ENTREGA CONVOCATORIA MAYO

# ENTREGA DE PRÁCTICA

## Datos

* Nombre: Adrián Montes Linares
* Titulación: Ingeniería Telemática
* Cuenta en laboratorios: adrian
* Cuenta URJC: a.montesl.2020
* Video básico (url): https://youtu.be/MP_jy5zef3Y
* Video parte opcional (url): https://youtu.be/sT0F2n62ypc
* Despliegue (url): https://adrian1.pythonanywhere.com/
* Contraseñas: Se indíca al principio de la práctica lo siguiente "No habrá autenticación de usuarios para acceder a las salas:" por lo que no hay contraseñas
* Cuenta Admin Site: admin/admin

## Resumen parte obligatoria

* El proyecto final del curso 2023-2024 consiste en la creación de una aplicación web llamada "TeVeO", que permite comentar lo que se ve en ciertas cámaras. La información de las cámaras se obtiene de fuentes soportadas. Los comentarios incluyen el momento en que se hicieron y una imagen de la cámara en ese momento. Cada cámara tiene un identificador único y una información asociada. No se requiere autenticación de usuarios para acceder a las salas.

La aplicación se construirá como un proyecto Django/Python3 con almacenamiento de datos en SQLite3. Se utilizarán plantillas Django para definir las páginas, y se proporcionarán páginas principales como la página de cámaras, página de cada cámara, página para poner un comentario, página dinámica de cada cámara, página de configuración y página de ayuda. Se utilizará HTMX para actualizar dinámicamente la página de la cámara y los comentarios.

El sitio también proporcionará cámaras en formato JSON y tendrá un mecanismo de autorización para permitir que otros navegadores accedan con la misma configuración. Se realizarán pruebas extremo a extremo y pruebas unitarias, aunque estas últimas son opcionales.

### Páginas de la práctica

#### Página Principal:
- **Contenido**: Listado de comentarios organizados de más nuevos a más viejos.
- **Elementos mostrados por comentario**: Identificador de la cámara (enlace a la página de la cámara), fecha del comentario, texto del comentario, imagen de la cámara en el momento del comentario.
- **Paginación**: Opcional.

#### Página de Cámaras:
- **Contenido**: 
  - Listado de fuentes de datos disponibles con botón para descargar.
  - Listado de todas las cámaras con imagen aleatoria en la parte superior.
- **Elementos mostrados por cámara**: 
  - Identificador de la cámara (enlace a la página de la cámara).
  - Enlace a la página dinámica de la cámara.
  - Nombre de la cámara.
  - Número de comentarios.
- **Orden**: Cámaras ordenadas por número de comentarios (de más a menos).

#### Página de Cada Cámara:
- **Contenido**:
  - Enlace a la página dinámica de la cámara.
  - Información de la cámara: nombre y localización.
  - Imagen actual de la cámara (tamaño del 50% del ancho disponible).
  - Enlace para escribir un comentario para la cámara.
  - Listado de todos los comentarios para esa cámara (ordenados de más recientes a más antiguos).

#### Página para Poner un Comentario:
- **Contenido**:
  - Formulario para poner un comentario.
  - Información de la cámara, imagen actual, fecha y hora.

#### Página Dinámica de Cada Cámara:
- **Contenido**:
  - Enlace a la página de la cámara.
  - Actualización periódica de la imagen y los comentarios cada 30 segundos.
  - Formulario para poner un comentario (carga dinámica).

#### Página de Configuración:
- **Contenido**:
  - Formulario para elegir el nombre del comentador.
  - Formulario para elegir elementos de apariencia personalizables (tamaño y tipo de letra).

#### Página de Ayuda:
- **Contenido**: 
  - Información en HTML sobre la autoría de la práctica, su funcionamiento y documentación breve.

### Elementos Generales en Todas las Páginas HTML:

#### Cabecera:
- Texto del nombre del sitio ("TeVeO"), sobre una imagen de fondo. El texto será un enlace al recurso "/" del sitio.
- Se mostrará el nombre del comentador que se está utilizando desde ese navegador, o "Anónimo" si no se ha especificado uno.

#### Menú:
- Barra debajo de la cabecera con enlaces a las siguientes páginas (excepto si la opción apunta a la página actual):
  - Página principal (texto: "Principal").
  - Página de cámaras (texto: "Cámaras").
  - Página de configuración (texto: "Configuración").
  - Página de ayuda (texto: "Ayuda").
  - Página de acceso al "Admin Site" (texto: "Admin").

#### Pie de Página:
- Resumen de métricas: "Cámaras: XXX. Comentarios: YYY", siendo XXX el número de cámaras y YYY el número de comentarios en todo el sitio.

### Aspecto de las Páginas:
- Marcado HTML: Cada elemento general estará dentro de un elemento div con un atributo id en HTML.
- CSS: Se utilizarán hojas de estilo CSS para definir la apariencia del sitio, incluyendo color de fondo y de letra, y elementos personalizables como tamaño y tipo de letra.
- Bootstrap: Se utilizará Bootstrap para la maquetación (layout) de las páginas, asegurando su correcto funcionamiento en navegadores de escritorio y móviles.

### Adicionales Proporcionados por el Sitio:
- Cámaras en formato JSON: Se ofrecerá un recurso para cada cámara en formato JSON, incluyendo toda su información, incluido el número de comentarios.

### Autenticación:
- Todos los navegadores pueden acceder a toda la funcionalidad del sitio.
- Se habilitará un mecanismo para autorizar a otro navegador a acceder al sitio con la misma configuración, mediante un enlace de autorización en la página de configuración.

### Pruebas:
- Extremo a extremo: Se realizará al menos una prueba "extremo a extremo" para cada tipo de recurso de la práctica.
- Unitarios: Será conveniente realizar también pruebas unitarias para distintas partes del código.


## Lista partes opcionales

* Favicon: Se le ha añadido el favicon como un .ico
* Orden de comentarios: Se permite ordenar los comentarios de dos maneras según la antigüedad
* Orden de camaras: Se permite ordenar lso comentarios de dos maneras según el número de comentários
* Iconos en el footer: Se le han añadido dos iconos al footer, una cámara y un logo de chat
* Carousel imágenes: Se le ha añadido en la página principal un carrusel con todas las imágenes cargadas
* JSON de todas las imagenes: Se ha añadido la opción de JSON de todas las imágenes disponibles, además de para cada cámara que es la parte obligatória
* Generar enlace de autenticación: Se ha añadido un boton en la configuración para generar el enlace de autenticación, al clickar se mostrara un JSON con el enlace a copiar, haciendo el proceso más comodo al usuario
* Establecer sesión: Se ha añadido la opción de introducir el enlace de autenticación en la pagina de configuración, al clickar se establecera la sesión, haciendo el proceso más comodo al usuario
