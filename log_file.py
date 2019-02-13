# -*- coding: utf-8 -*-
"""
graba errors y avisos en un string que luego se puede grabar en un fichero
"""

import io


_contents = io.StringIO()
_DST = 'log.txt'


def contents_get():
    """
    devuelve el valor de _contents
    """
    return _contents.getvalue()


def write(*args):
    """
    escribe un valor en _contents
    """
    for arg in args:
        _contents.write('{}\n'.format(arg))


def to_file(dst=None):
    """
    graba el string _contents en un fichero
    """
    from time import gmtime, strftime
    from os.path import join

    msg = _contents.getvalue()

    if dst:
        fo = open(join(dst, _DST), 'w')
    else:
        fo = open(_DST, 'w')
    fo.write('{}'.format(strftime("%a, %d %b %Y %H:%M:%S +0000\n\n", gmtime())))
    if msg:
        fo.write('{}'.format(msg))
    fo.close()
