from  glob import iglob
import shutil
import os
import sys
import ConfigParser
import time

def ConvertirFichero(fichero):
	os.system("ffmpeg -i " + rutaActual + "/" + fichero + " -an -sameq -y -s "+ resolucion+" "+ rutaTemporal + fichero + extensionSalida)

def BorrarTemporal():
	shutil.rmtree(rutaTemporal)

def CrearRutaTemporal():
	if not os.path.exists(rutaTemporal):
		os.mkdir(rutaTemporal)

def CrearRutaFinal():
	if not os.path.exists(rutaFinal):
		os.mkdir(rutaFinal)

def ConvertirFicherosDelDirectorio():
	for name in os.listdir(rutaActual):
		ConvertirFichero(name)
	
def CrearFicheroFinal():
	fecha = time.localtime()

	#refactorizar
	ficheroFinal = str(fecha[0]) + str(fecha[1]) + str(fecha[2]) + str(fecha[3]) + str(fecha[4]) + str(fecha[5]) + ".avi"

	destino = open(rutaTemporal + 'salidaTemp','wb')

	for filename in iglob(os.path.join(rutaTemporal,'*.avi')):
		#print filename
		shutil.copyfileobj(open(filename,'rb'), destino)

	destino.close()

	os.system("ffmpeg -i " + rutaTemporal + "salidaTemp -sameq " + rutaFinal + ficheroFinal)


cfg = ConfigParser.ConfigParser()
if not cfg.read(["./tratvid.cfg"]):
	print "No existe el archivo de configuracion"	

rutaActual		= os.path.realpath(sys.argv[1])
resolucion      = cfg.get("video","resolucion")
rutaTemporal    = rutaActual + cfg.get("rutas","temporal")
rutaFinal		= rutaActual + cfg.get("rutas","final")
extensionSalida = cfg.get("salida","extension")

CrearRutaTemporal()

CrearRutaFinal()

ConvertirFicherosDelDirectorio()

CrearFicheroFinal()

BorrarTemporal()
