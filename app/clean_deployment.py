# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

from app.delete_target import delete_target
from app.deployment_descriptor import DeploymentDescriptor


def clear_deployment(fin: str):
    dd = DeploymentDescriptor(fin)
    target_dir = dd.get_target_dir()
    delete_target(target_dir)
    return


if __name__ == '__main__':
    clear_deployment('../deployment.txt')
