# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

from pathlib import Path


def delete_target(_target: Path):
    assert _target.is_dir()

    for item in _target.glob('*'):
        if item.is_dir():
            delete_target(item)
            try:
                item.unlink()
                print(f'unlink dir: {item}')
            except PermissionError as e:
                pass
        elif item.is_file():
            item.unlink()
            print(f'unlink file: {item}')
        else:
            raise Exception(item)
    return
