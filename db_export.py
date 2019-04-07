# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 13:12:53 2019

@author: Solis
SELECT * FROM MSysObjects WHERE Type=1 AND Flags=0;
SELECT * FROM MSysRelationships;
"""

header_sql_file = ('SET CLIENT_ENCODING TO UTF8;',
                   'SET STANDARD_CONFORMING_STRINGS TO ON;')

# número de líneas separadoras en los ficheros output
NHYPHEN = 70

# molde para fichero FILE_COPYFROM metacomando de psql
copyfrom = ("\copy {} ({}) ",
            "from '{}' ",
            "with (format csv, header, delimiter ',', encoding 'LATIN1',",
            " force_null ({}))")


def constring_get(db):
    """
    conexion string general para ficheor mdb y accdb
    """
    a = 'DBQ={0};'.format(db)
    conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; ' + a
    return conn_str


def access_types_in_db():
    """
    gets access columns types in databese db
    IN
    db (str)
    OUT
    mytypes ([str]): list with access type names in db
    Cadena de conexión
    """
    import pyodbc
    from db_export_parameters import db

    con = pyodbc.connect(constring_get(db))
    cur = con.cursor()
    tables = [table[2] for table in cur.tables() if table[3] == 'TABLE']
    print('{0:d} tables found'.format(len(tables)))

    acc_types = []
    for table_name in tables:
        types_in_table = [row.type_name
                          for row in cur.columns(table=table_name)]
        for type1 in types_in_table:
            if type1 not in acc_types:
                acc_types.append(type1)
    return acc_types


def ms_access_structure_get():
    """
    extracts tables column names and call function thar write each
    table structure
    input:
        db (str): access data base file (must exist)
        dir_out (str): output directory (must exists)
    """
    FILE_TABLES_NAMES = '_TABLES_NAMES.txt'
    FILE_CREATE_TABLES = '_CREATE_TABLES.sql'
    FILE_RELATIONSHIPS = '_CREATE_FOREIGNKEYS.sql'
    FILE_COPYFROM = '_COPYFROM.txt'

    from os.path import join
    import pyodbc
    from db_export_parameters import db, dir_out, wstruct, wdata
    from db_export_parameters import trelationships

    cns = constring_get(db)
    con = pyodbc.connect(cns)
    cur = con.cursor()
    tables = [table[2] for table in cur.tables() if table[3] == 'TABLE']
    print('{0:d} tables found'.format(len(tables)))

    if wstruct == 1:
        fo = open(join(dir_out, FILE_CREATE_TABLES), 'w')
        fo.write('{}'.format('\n'.join(header_sql_file)))
        focopyfrom = open(join(dir_out, FILE_COPYFROM), 'w')

    if wdata == 1:
        focopyfrom = open(join(dir_out, FILE_COPYFROM), 'w')

    table_names = []
    for i, table_name in enumerate(tables):
        print('{0:d}. {1}'.format(i+1, table_name))
        table_names.append(table_name)
        # columnas
        columns = [[row.ordinal_position, row.column_name, row.type_name,
                    row.column_size, row.nullable, row.remarks]
                   for row in cur.columns(table=table_name)]
        # primary keys
        pk_cols = [[row[7], row[8]]
                   for row in cur.statistics(table_name)
                   if row[5] is not None and
                   row[5].upper() == 'PRIMARYKEY']

        if wstruct == 1:
            write_table_struct(fo, table_name, columns, pk_cols)

        if wdata == 1:
            field_names = [column[1] for column in columns]
            write_data(table_name, field_names, con, dir_out)
            sfield_names = ','.join(field_names)
            write_copyfrom(table_name, sfield_names, dir_out, focopyfrom)

    if wdata == 1:
        focopyfrom.close()

    if wstruct == 1:
        fo.close()
        fo = open(join(dir_out, FILE_RELATIONSHIPS), 'w')
        fo.write('beguin;\n')
        cur.execute('SELECT * FROM {};'.format(trelationships))
        fks = [row for row in cur.fetchall()]
        for row in fks:
            fo.write('\n')
            fo.write('alter table if exists {} '.
                     format(row.szObject))
            fo.write('drop constraint if exists {};\n'.
                     format(row.szRelationship))

            fo.write('alter table if exists {}\n'.
                     format(row.szObject))
            fo.write('add constraint {} '.
                     format(row.szRelationship))
            fo.write('foreign key ({}) '.
                     format(row.szColumn))
            fo.write('references {0} ({1});'.
                     format(row.szReferencedObject, row.szReferencedColumn))
            fo.write(2*'\n')
            fo.write(NHYPHEN*'-' + '\n')
        fo.write('commit;\n')
        fo.close()

    table_names_str = '\n'.join(table_names)
    fo = open(join(dir_out, FILE_TABLES_NAMES), 'w')
    fo.write('{}'.format(table_names_str))
    fo.close()


def translate_msa(atype, length):
    """
    translates ms access types to postgis types
    """
    ttypes = {'TEXT': 'varchar', 'VARCHAR': 'varchar',
              'MEMO': 'varchar', 'LONGCHAR': 'varchar',
              'BYTE': 'smallint', 'INTEGER': 'integer', 'LONG': 'bigint',
              'SMALLINT': 'smallint',
              'SINGLE': 'real', 'DOUBLE': 'double precision',
              'REAL': 'double precision',
              'CURRENCY': 'money', 'AUTONUMBER': 'serial',
              'COUNTER': 'serial',
              'DATETIME': 'timestamp',
              'YES/NO': 'smallint'}
    if atype in('TEXT', 'VARCHAR', 'MEMO', 'LONGCHAR') and length > 0:
        return '{}({})'.format(ttypes[atype], length)
    else:
        return ttypes[atype]


def write_table_struct(fo, table_name, columns, pk_cols):
    """
    writes table structure in text file fo
    fo (object file): text file (must be open)
    table_name (str)
    columns [[]]: columns definition (defined in ms_access_structure_get)
    """
    fo.write(2*'\n')
    fo.write('drop table if exists {}\nbeguin;\n'.format(table_name))
    fo.write('create table if not exists ' + table_name + '(\n')
    wcolumns = ['\t{} {}'.format(column[1],
                translate_msa(column[2], column[3])) for column in columns]
    fo.write(',\n'.join(wcolumns))
    fo.write('\n')
    pk_columns = [row[1] for row in pk_cols]
    if len(pk_columns) > 0:
        pk_cstr = ','.join(pk_columns)
        fo.write('\tconstraint {0} primary key ({1})\n'.format(table_name,
                 pk_cstr))
    fo.write(');\n'+'commit;\n')
    fo.write(NHYPHEN*'-' + '\n')


def csv_file_name_get(dir_out, table_name):
    from os.path import join
    return join(dir_out, table_name + '.csv')


def write_data(table_name, field_names, con, dir_out):
    """
    writes all table data
    in
    table_name (str)
    field_names ([str,...])
    con (object connexion to an access data base)
    dir_out (str): directory to write data (must exists)
    """
    import csv
    csv_file = csv_file_name_get(dir_out, table_name)

    cur = con.cursor()
    cur.execute('select * from [' + table_name + '];')

    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_NONNUMERIC,
                            lineterminator='\n')
        writer.writerow(field_names)
        for row in cur:
            writer.writerow(row)


def write_copyfrom(table_name, sfield_names, dir_out, fo):
    """
    writes \copy .. from psql metacommand one for each table
    """
    stm = ''.join(copyfrom)
    csv_file = csv_file_name_get(dir_out, table_name)
    stm1 = stm.format(table_name, sfield_names, csv_file, sfield_names)
    fo.write('{}\n\n'.format(stm1))
