__author__ = "Skylaw6"
__version__ = "1.0.0"
__contact__ = "skylaw6@hotmail.com"

import obspython as obs
from random import seed
from random import randint
import datetime

interval    = 30
source_name = ""
file_path = ""

#-----funcion principal
def update_text(): 
	global interval
	global source_name
	global file_path

	source = obs.obs_get_source_by_name(source_name)
	
	#---aqui va el generador de numeros aleatorios y lectura de archivo con texto

	#--apertura y lectura del archivo de frases
	frases=[]
	contador=0

	if file_path!="":
		file=open(file_path, "r")
		for line in file:
			print(line[:-1])
			frases=frases+[line[:-1]]
			contador=contador+1
		file.close()
		#generador de numeros aleatorios enteros usando como semilla la fecha
		now=datetime.datetime.now()
		semilla=now.day+now.month+now.year+now.hour+now.minute+now.second
		seed(semilla)
		valor=randint(0,contador-1)
		text=frases[valor]

	if file_path=="":
		text="Archivo no seleccionado"

	#------carga de un objeto de datos para obs en "settings", el texto y la fuente en la que se escribe
	settings = obs.obs_data_create()
	obs.obs_data_set_string(settings, "text", text)
	obs.obs_source_update(source, settings)
	obs.obs_data_release(settings)
	obs.obs_source_release(source)

#-----------------funcion definida que lanza la funcion principal cuando se presiona le boton
def refresh_pressed(props, prop): 
	update_text()


#---------------Funcion que carga la descripcion del script
def script_description():
	return "Muestra textos desde un archivo.\n\nPor Skylaw6"

#funcion que s elanza cada vez que algun parametro es actualizado por el usuario
def script_update(settings):
	global interval
	global source_name
	global file_path

	interval    = obs.obs_data_get_int(settings, "interval")
	source_name = obs.obs_data_get_string(settings, "source")
	file_path = obs.obs_data_get_string(settings, "file")

	obs.timer_remove(update_text)
	if file_path != "" and source_name != "":
		obs.timer_add(update_text, interval * 1000)

#----------------------Funcion que carga valores por default
def script_defaults(settings):
	obs.obs_data_set_default_int(settings, "interval", 10)


#-----Funcion que carga las variables en un arreglo de datos de tipo propiedades de la api de obs, son la interfz grafica que se ve en la seccion de scripts
def script_properties():

	props = obs.obs_properties_create()

	#campo de directorio
	obs.obs_properties_add_path(props,"file","Archivo de frases",obs.OBS_PATH_FILE,"*.txt","")

	#campo de lectura d enumeros enteros
	obs.obs_properties_add_int(props, "interval", "Intervalo de \nactualizacion (segundos)", 5, 3600, 1)

	#una combo list que meustra todas las fuentes de tipo texto
	p = obs.obs_properties_add_list(props, "source", "Fuente de texto", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
	sources = obs.obs_enum_sources()
	if sources is not None:
		for source in sources:
			source_id = obs.obs_source_get_unversioned_id(source)
			if source_id == "text_gdiplus" or source_id == "text_ft2_source":
				name = obs.obs_source_get_name(source)
				obs.obs_property_list_add_string(p, name, name)

		obs.source_list_release(sources)
	#un boton que lanza la funcion update_text cuando se presiona
	obs.obs_properties_add_button(props, "button", "Refrescar", refresh_pressed)
	return props