# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

import os
from pathlib import Path


def resolve_directory_name(_dir: Path, item: str) -> Path:
    item = resolve_environment_variables(item)
    result = _dir / item
    result = result.resolve()
    return result


def resolve_environment_variables(item: str) -> str:
    if '%' not in item:
        return item

    cnt = item.count('%')
    x = cnt % 2
    if x != 0:
        raise Exception(f'wrong environment variable: {item}')

    prefix, _residual = item.split('%', 1)
    term, postfix = _residual.split('%', 1)

    postfix = resolve_environment_variables(postfix)

    try:
        term = os.environ[term]
    except KeyError:
        raise Exception(f'ENV VAR doesn\'t exist {term}')

    return prefix + term + postfix
