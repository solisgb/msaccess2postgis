# -*- coding: utf-8 -*-
"""
módulo con la asignación de los parámetros del programa
también se explica el significado de cada parámetro
@solis
"""
# _________________DATOS_______________________

# ruta a la base de datos Access para hacer backup
db = r'C:\Users\solis\Documents\DB\Ipasub97.mdb'

# nombre de la tabla copia de relationships (tabla del sistema)
trelationships = '_msysrelationships'

# directorio de resultados
dir_out = r'C:\Users\solis\Documents\DB\bak'

# ______________VARIABLES QUE CONTROLAN LAS ACCIONES DEL SCRIPT_______________
"""get_types [0, 1]
   si 1 muestra los tipos de las tablas Access y su relación con los tipos
   psql
   si 1 el script no realiza ninguna acción más, independientemente de los
   valores del resto de variables"""
get_types = 0

"""wstruct [0, 1]
   si 1 crea la la sentencia psql para crear cada una de las tablas de la
   base de datos Access"""
wstruct = 0

""" wdata [0, 1]
    si 1 copia los datos de cada tabla en formato csv y crea un fichero
    con las sentencias copy tabla (...) from file with (...)"""
wdata = 1
