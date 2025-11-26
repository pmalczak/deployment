# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

import copy
import shutil
from pathlib import Path

from app.copy_content import copy_content
from app.deployment_descriptor import DeploymentDescriptor, SourceDoesNotExists


def deployment_proc(cwd: Path, fin: Path):
    dd = DeploymentDescriptor(fin)
    target = dd.get_target_dir()
    if isinstance(target, Path):
        dd.target_dir = target
        _single_target(dd, cwd, fin)
    elif isinstance(target, list):
        for _target in target:
            _dd = copy.copy(dd)
            _dd.target_dir = _target
            _single_target(_dd, cwd, fin)


def _single_target(dd, cwd, fin):
    try:
        lst = dd.prepare_copy_descriptor()
    except SourceDoesNotExists as e:
        msg = f'Wrong descriptor:\n{e}\n'
        print(msg)
        return

    for item in lst:
        copy_content(item)

    name = fin.name.split('.')
    assert len(name) == 2
    name = name[0]

    method = 'zip'
    if dd.target_format == method:
        target_dir = dd.get_target_dir()
        shutil.make_archive(name, method, root_dir=target_dir)
        print(f'target: {cwd}\\{name}.{method}')

    return
