# -*- coding: utf-8 -*-
"""
dbexport_main; script para pasar mdb a ficgeros psql

@solis
"""

db = r'\\ESMUR0001\hidrogeologia\BD_IPASUB\Ipasub97.mdb'
dir_out = r'\\ESMUR0001\hidrogeologia\BD_IPASUB\STRUCT2POSTGRES'
get_types = 0
wstruct = 1
wdata = 0

if __name__ == "__main__":

    try:
        from datetime import timedelta
        from time import time
        import log_file as lf
        from db_export import ms_access_structure_get, access_types_in_db

        startTime = time()

        if get_types == 1:
            mytypes = access_types_in_db(db)
            for type1 in mytypes:
                print(type1)
        else:
            ms_access_structure_get(db, dir_out, wstruct, wdata)

        xtime = time()-startTime
        print('The script took {0}'.format(str(timedelta(seconds=xtime))))
    except Exception as e:
        import traceback
        import logging
        msg = '\n{}'.format(traceback.format_exc())
        logging.error(msg)
        lf.write(msg)
    finally:
        lf.write('last execution was ok')
        lf.to_file()
        print('fin; se ha generado el fichero log.txt')
