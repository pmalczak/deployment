# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

import os
import shutil


def copytree(src: str, dst: str, exclude: str = '', symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if not _check_exclusion(s, exclude):
                copytree(s, d, exclude=exclude, symlinks=symlinks, ignore=ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                if _check_exclusion(s, exclude):
                    break
                shutil.copy2(s, d)
                print(f'copy {d}')


def _check_exclusion(dst, exclusion: str) -> bool:
    exclusions = exclusion.split('|')
    for item in exclusions:
        if item and item in dst:
            return True
    return False
