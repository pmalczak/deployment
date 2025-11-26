# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

from pathlib import Path
from app.resolve_directory_name import resolve_directory_name


class SourceDoesNotExists(Exception):
    pass


class DeploymentDescriptor:
    def __init__(self, deployment_descriptor_file: Path):
        self.deployment_descriptor_file_name = deployment_descriptor_file
        self.target_dir = None
        self.target_format = None

    def get_target_dir(self) -> (Path, tuple):
        if self.target_dir is not None:
            return self.target_dir
        cwd = Path().cwd()
        lst = self._read_file_content()
        lst = list(filter(lambda x: not x.startswith('#'), lst))
        target_dir = None
        for item in lst:
            if item.startswith('target_dir='):
                item = item.split('=')
                item = item[1]

                item = item.split('|')
                if len(item) == 1:
                    target_dir = resolve_directory_name(cwd, item[0])
                    if not target_dir.is_dir():
                        x = self._where_exactly_(target_dir)
                        raise NotADirectoryError(x)
                    break
                else:
                    target_dir = []
                    for _item in item:
                        _r = resolve_directory_name(cwd, _item)
                        if not _r.is_dir():
                            raise NotADirectoryError(str(_r))
                        target_dir += [_r]
                    break

        return target_dir

    def _where_exactly_(self, path: Path) -> Path:
        while True:
            if path.parent.is_dir():
                return path
            path = path.parent

    def prepare_copy_descriptor(self) -> list:
        lst = self._read_file_content()
        lst = list(filter(lambda x: not x.startswith('#'), lst))
        lst = list(filter(lambda x: x != '', lst))
        result = self._as_raw_descriptor(lst)
        result = self._resolve_descriptor_items(result)
        return result

    def _read_file_content(self) -> list:
        with open(self.deployment_descriptor_file_name, 'r') as f:
            s = f.read()

        lst = s.split('\n')
        return lst

    def _as_raw_descriptor(self, lst) -> list:
        result = []
        cwd = Path().cwd()
        item_to = None
        copy_from = None

        for item in lst:
            if 'target_dir' in item:
                assert isinstance(self.target_dir, Path)
                assert self.target_dir.is_dir()

            elif 'target_format' in item:
                expected_formats = ('zip', 'catalog')
                item = item.split('=')
                item = item[1]
                if item not in expected_formats:
                    raise Exception(f'expected format: {expected_formats} got: "{item}" instead')
                self.target_format = item

            elif 'copy_from=' in item:
                _item = item.split('=', 1)
                _item = _item[1]

                _item = _item.split(':copy_to=')
                item_from = _item[0]
                try:
                    item_to = _item[1]
                    item_to = resolve_directory_name(self.target_dir, item_to)
                except IndexError:
                    item_to = None

                copy_from = resolve_directory_name(cwd, item_from)
                if not copy_from.is_dir():
                    raise Exception(f'copy_from item doesn\'t exist: {copy_from}')
            else:
                assert copy_from is not None
                assert self.target_dir is not None
                item = item.strip()

                if item_to is not None:
                    assert isinstance(item_to, Path)
                    copy_to = item_to
                else:
                    copy_to = self.target_dir
                _r = copy_from, copy_to, item
                result += [_r]

        assert self.target_dir is not None
        assert self.target_format is not None
        return result

    def _resolve_descriptor_items(self, _raw_descriptor: list) -> list:
        descriptor = []
        for _item in _raw_descriptor:
            copy_from, target_dir, item = _item
            assert isinstance(copy_from, Path)

            if '*' in item:
                descriptor += [(copy_from, target_dir, item)]
            else:
                _src = copy_from / item
                _src = _src.resolve()
                if not _src.exists():
                    msg = f'file: {self.deployment_descriptor_file_name} item:{item}'
                    raise SourceDoesNotExists(msg)

                _target = target_dir / item
                _target = _target.resolve()
                descriptor += [(_src, _target, item)]
        return descriptor
