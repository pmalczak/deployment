# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

import glob
import os
import shutil
from pathlib import Path


def recursive_copy(_source: Path, _target: Path, item: str):
    os.chdir(_source)
    _recursive_copy_(_source, _target, item)
    return


def _recursive_copy_(_source: Path, _target: Path, item: str):
    for _source_file in glob.glob(item):
        assert isinstance(_source_file, str)
        _source_file_path = _source / _source_file
        _target_file_path = _target / _source_file
        _copy_copy2(_source_file_path, _target_file_path)

    for iter_elem in glob.glob('*'):
        _s = _source / iter_elem
        if _s.is_dir():
            _t = _target / iter_elem
            recursive_copy(_s, _t, item)
    return


def _copy_copy2(_source_file, _target_file: Path):
    assert isinstance(_target_file, Path)
    create_missing_paths(_target_file.parent)
    if not os.path.exists(_target_file) or (os.stat(_source_file).st_mtime - os.stat(_target_file).st_mtime) > 1:
        shutil.copy2(_source_file, _target_file)
        print(f'copy {_target_file}')
    return


def create_missing_paths(_path: Path):
    if _path.is_file():
        return

    if not _path.parent.is_dir():
        create_missing_paths(_path.parent)

    if not _path.is_dir():
        os.mkdir(_path)
    return
