# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 13:12:53 2019

@author: Solis
"""


def access_types_in_db(db):
    """
    gets access columns types in databese db
    IN
    db (str)
    OUT
    mytypes ([str]): list with access type names in db
    """
    import pyodbc
    import db_con_str

    con = pyodbc.connect(db_con_str.con_str(db))

    cur = con.cursor()
    tables = [table[2] for table in cur.tables() if table[3] == 'TABLE']
    print('{0:d} tables found'.format(len(tables)))

    my_types = []
    for table_name in tables:
        types_in_table = [row.type_name
                          for row in cur.columns(table=table_name)]
        for type1 in types_in_table:
            if type1 not in my_types:
                my_types.append(type1)
    return my_types


def ms_access_structure_get(db, dir_out, wstruct=1, wdata=0):
    """
    extracts tables column names and call function thar write each
    table structure
    input:
        db (str): access data base file (must exist)
        dir_out (str): output directory (must exists)
    """
    FILE_NAME = '_DB_STRUCTURE.sql'

    from os.path import join
    import pyodbc
    import db_con_str

    con = pyodbc.connect(db_con_str.con_str(db))

    cur = con.cursor()
    tables = [table[2] for table in cur.tables() if table[3] == 'TABLE']
    print('{0:d} tables found'.format(len(tables)))

    if wstruct == 1:
        fo = open(join(dir_out, FILE_NAME), 'w')

        for i, table_name in enumerate(tables):
            print('{0:d}. {1}'.format(i+1, table_name))
            columns = [[row.ordinal_position, row.column_name, row.type_name,
                        row.column_size, row.nullable, row.remarks]
                       for row in cur.columns(table=table_name)]
            pk_cols = [[row[7], row[8]]
                       for row in cur.statistics(table_name)
                       if row[5] is not None and
                       row[5].upper() == 'PRIMARYKEY']

            write_table_struct(fo, table_name, columns, pk_cols)
            if wdata == 1:
                field_names = [column[1] for column in columns]
                write_data(table_name, field_names, con, dir_out)
        fo.close()


def translate_msa(atype, length):
    """
    translates ms access types to postgis types
    """
    ttypes = {'TEXT': 'varchar', 'VARCHAR': 'varchar',
              'MEMO': 'varchar', 'LONGCHAR': 'varchar',
              'BYTE': 'smallint', 'INTEGER': 'integer', 'LONG': 'bigint',
              'SMALLINT': 'integer',
              'SINGLE': 'real', 'DOUBLE': 'double precision',
              'REAL': 'double precision',
              'CURRENCY': 'money', 'AUTONUMBER': 'serial',
              'COUNTER': 'serial',
              'DATETIME': 'timestamp',
              'YES/NO': 'varchar(3)'}
    return ttypes[atype]


def write_table_struct(fo, table_name, columns, pk_cols):
    """
    writes table structure in text file fo
    fo (object file): text file (must be open)
    table_name (str)
    columns [[]]: columns definition (defined in ms_access_structure_get)
    """

    fo.write('create table if not exists ' + table_name + '(\n')
    fo.write('\tgid serial primary key\n')
    for column in columns:
        fo.write('\t{} {}\n'.format(column[1], translate_msa(column[2],
                 column[3])))
    pk_columns = [row[1] for row in pk_cols]
    if len(pk_columns) > 0:
        pk_cstr = ','.join(pk_columns)
        fo.write('\tconstraint unique ({})\n'.format(pk_cstr))

    fo.write(');\n\n')


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
    from os.path import join
    csv_file = join(dir_out, table_name + '.csv')

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
