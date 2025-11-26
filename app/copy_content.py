# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

import os
from pathlib import Path

from app.copy_tree import copytree
from app.recursive_copy import recursive_copy, _copy_copy2


def copy_content(arg: tuple):
    _source, _target, item = arg

    if '*' not in item:
        if _source.is_dir():
            copytree(str(_source), str(_target), exclude='.pyc|.git')
        elif _source.is_file():
            _copy_copy2(_source, _target)
        else:
            raise Exception

    elif item.startswith('r:'):
        item = item.split('r:')
        item = item[1]
        cwd = os.getcwd()
        try:
            recursive_copy(_source, _target, item)
        finally:
            os.chdir(cwd)

    else:
        for _source_file in _source.glob(item):
            assert isinstance(_source_file, Path)
            _target_file = _target / _source_file.name
            _copy_copy2(_source_file, _target_file)
    return
