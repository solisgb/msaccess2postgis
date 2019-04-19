# msaccess to postgres
It reads the tables definition from a ms access database and write a sql file with create tables sql sentences, using pyodbc.
pyodbc can not retrieves foreign keys directly because of the driver; I make a copy of MsysRelationShips and then I can read it.
Now the script only manages one field primary keys and foreign keys. Optionally, you can make a copy of all the tables in csv format and write a sql file with psql sentences to import the data.

You can modify the string connection to change the DMS; in this case you must write a short piece of code to read foreign keys.

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
