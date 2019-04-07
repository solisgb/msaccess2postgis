# -*- coding: utf-8 -*-
"""
dbexport_main; script para:
    1 muestra los tipos exitentes en una BDD access
      y su correspondencia con los tipos postgres
    2 escribe las sentencias psql para crear cada una de las tablas de
      la base de datos Access
      en la actualidad no soporta primary keys o foreign relations
      formadas por varios campos
    3 Hacer una copia de todos los datos de cada tabla en ficheros csv

Los datos del script y las opciones al ejecutar el script se definen
    por el usuario en el módulo db_export_parameters.py
Las opciones de ejecución son:
    get_types = 1 (1)
    wstruct = 1 (2)
    wdata = 1 (3)
    wstruct = 1 y wdata = 1 (2 y 3)

El controlador de Acces no permite a pyodbc obtener las foreign keys de la
BDD; tampoco me permite hacer una select a la tabla MsysRelationShips

Para solventarlo es necesario hacer una copia del fichero interno se Access
MsysRelationShips (select * from msysrelationships) y guardarlo en una
tabla con otro nombre. De esta tabla ya se puede hacer una select para obtener
las foreign keys.

Warning. Actualizar la tabla de relaciones antes de ejecutarlo el script
para asegurarse que entran todas

@solis
"""


if __name__ == "__main__":

    try:
        from datetime import timedelta
        from time import time
        import db_export_parameters as par
        import log_file as lf
        import db_export as dbe

        startTime = time()

        if par.get_types == 1:
            mytypes = dbe.access_types_in_db(par.db)
            for type1 in mytypes:
                try:
                    psql_type = dbe.translate_msa(type1)
                except Exception as e:
                    psql_type = 'No encontrado'
                print('{} -> {}'.format(type1, psql_type))
            print('\nSi observas algún error puedes modificar el' +
                  'diccionario en translate_msa, módulo db_export')
        else:
            dbe.ms_access_structure_get()

        xtime = time()-startTime
        print('The script took {0}'.format(str(timedelta(seconds=xtime))))
    except Exception as e:
        import traceback
        import logging
        msg = '\n{}'.format(traceback.format_exc())
        logging.error(msg)
        lf.write(msg)
    else:
        lf.write('last execution was ok')
    finally:
        lf.to_file()
        print('fin; se ha generado el fichero log.txt')
