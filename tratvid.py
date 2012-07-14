from  glob import iglob
import signal
import shutil
import os
import sys
import ConfigParser
import time

def TamanoTotalArchivosEnCarpeta():
	tamanoTotal = 0
	for fichero in os.listdir(rutaActual):
		if os.path.isfile(rutaActual + "/" + fichero):
			tamanoTotal = tamanoTotal + ((os.path.getsize(rutaActual+"/"+fichero) / 1024 ) / 1024)
	return tamanoTotal

 
def ConvertirFichero(fichero):
	print "Convirtiendo el fichero: " + rutaActual + "/" + fichero
	os.system("avconv -i " + rutaActual + "/" + fichero + " -vcodec "+ videoCodec + " -threads "+ threads + " -vb "+ bitrate +" -an -y -s "+ resolucion+" -pass 2 "+ rutaTemporal + fichero + extensionSalida + " 2>> " + rutaLogs + ficheroFinal + ".log")
os.system("avconv -i " + rutaActual + "/" + fichero + " -vcodec "+ videoCodec + " -threads "+ threads + " -vb "+ bitrate +" -an -y -s "+ resolucion+" -pass 2 "+ rutaTemporal + fichero + extensionSalida + " 2>> " + rutaLogs + ficheroFinal + ".log")

def EliminarFichero(fichero):
	if (cfg.get("opciones","eliminaroriginal") == "1"):
		print "Eliminando el fichero: " + fichero
		os.remove(fichero)

def BorrarTemporal():
	if (cfg.get("opciones","eliminartemporal") == "1"):
		print "Eliminando el directorio temporal"
		shutil.rmtree(rutaTemporal)

def CrearRutaTemporal():
	if not os.path.exists(rutaTemporal):
		print "Creando el directorio temporal"
		os.mkdir(rutaTemporal)

def CrearRutaFinal():
	if not os.path.exists(rutaFinal):
		print "creando el directorio final"
		os.mkdir(rutaFinal)

def CrearRutaLogs():
	if not os.path.exists(rutaLogs):
		print "creando el directorio de logs"
		os.mkdir(rutaLogs)	

def CrearCarpetas():
	CrearRutaTemporal()
	CrearRutaFinal()
	CrearRutaLogs()

def ConvertirFicherosDelDirectorio():
	for name in os.listdir(rutaActual):
		if os.path.isfile(rutaActual + "/" + name):
			ConvertirFichero(name)
			EliminarFichero(rutaActual + "/" + name)
	
def CrearFicheroFinal():
	print "Creando el fichero final: " + rutaFinal + ficheroFinal + extensionSalida
	
	destino = open(rutaTemporal + ficheroTemporal,'wb')

	for filename in sorted(iglob(os.path.join(rutaTemporal,'*.avi'))):
		shutil.copyfileobj(open(filename,'rb'), destino)

	destino.close()

	os.system("ffmpeg -i " + rutaTemporal + ficheroTemporal + " -sameq " + rutaFinal + ficheroFinal + extensionSalida + " 2>> " + rutaLogs + ficheroFinal + ".log")


def NombreFinal():
	fecha = time.localtime()

	ficheroFinal = ''	

	for i in range(6):
		ficheroFinal = ficheroFinal + str(fecha[i])

	return ficheroFinal	

def Ejecutar():
	
	NombreFinal()

	CrearCarpetas()

	ConvertirFicherosDelDirectorio()

	CrearFicheroFinal()

	BorrarTemporal()
	
def MostrarMensajeEspera():
	print ""
	print "A la espera...(Puede parar el proceso con Ctrl-C"
	print ""
	print ""

cfg = ConfigParser.ConfigParser()
if not cfg.read(["./tratvid.cfg"]):
	print "No existe el archivo de configuracion"	

rutaActual = os.path.realpath(sys.argv[1])
resolucion = cfg.get("video","resolucion")
videoCodec = cfg.get("video","codec")
threads = cfg.get("video","threads")
bitrate = cfg.get("video","bitrate")
rutaTemporal = rutaActual + cfg.get("rutas","temporal")
rutaFinal =  rutaActual + cfg.get("rutas","final")
rutaLogs = rutaActual + cfg.get("rutas","logs")
extensionSalida = cfg.get("salida","extension")
ficheroTemporal = cfg.get("salida","ficherotemporal")
ficheroFinal = NombreFinal()

if ( sys.argv[2] == '-d'):
	print "INICIADA LA APLICACION TratVid"
	MostrarMensajeEspera()
	
	while True:
		time.sleep(int(cfg.get("opciones","tiempoespera")))
		
		if (TamanoTotalArchivosEnCarpeta() > int(cfg.get("opciones","maxtamano"))): 
			Ejecutar()
			MostrarMensajeEspera()
			
else:
	Ejecutar()
