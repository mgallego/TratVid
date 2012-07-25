TratVid
=======

Se trata de un pequeño script realizado con Python para coger todos los vídeos de una carpeta, comprimirlos, recodificarlos y unirlos.

Lo he creado como utilidad para unir los clips que genera mi cámara de video y poder reproducirlos en el formato deseado.

Dependencias
------------

### ffmpeg / avconv
### avidemux2_cli
### libavcodec-extra-53


Uso
---

### Fichero de cofiguración
Parámetros:
#### [video]
* resolucion: Resolución del video
* codec: codec de compresión de video
* bitrate: bitrate de compresión de video
* threads: número de hilos

#### [Audio]
* codec: codec a utilizar (Sin implementar aún)

#### [rutas]
* temporal: directorio donde se guardarán los ficheros temporales
* final: directorio donde se guardarán los ficheros finales
* logs: directorio donde se guardarán los logs

Estos directorios son creados automáticamente por la aplicación en caso de no existir

#### [salida]
* extension: extensión para el fichero de salida
* ficherotemporal: nombre del fichero temporal que se crea para unir todos los ficheros tratados

#### [opciones]
* eliminartemporal: [0,1] Elimina el directorio temporal al acabar la ejecución
* eliminaroriginal: [0,1] Elimina el fichero original tras procesarlo
* maxtamano: (demonio) máximo tamaño que debe tener la carpeta para que empiece la ejecución
* tiempoespera: (demonio) tiempo de espera entre comprobaciones de tamaño de directorio



TratVid
=======

This is a small Python script to get done with all the videos in a folder, compress, recode and merge.

I created it as useful for attaching clips that generates my video camera and play them in the desired format.to deseado.

Dependencies
------------

**ffmpeg / avconv**
**avidemux2_cli**
**libavcodec-extra-53**