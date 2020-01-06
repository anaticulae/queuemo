# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import link
import utila

import queuemo
import tests.resources


def install_requirements():
    """Install queuemo and run queuemo --help to ensure basic function"""
    uninstall = 'pip uninstall queuemo -y'
    install = 'python setup.py install && queuemo --help'

    clean_and_run = uninstall + ' && ' + install
    completed = utila.run(clean_and_run, cwd=queuemo.ROOT)  # run setup.py
    assert completed.returncode == utila.SUCCESS, str(completed)


def sync_resources():
    completed = utila.run('power --all', cwd=tests.resources.PDF)  # pylint:disable=C0103
    assert completed.returncode == utila.SUCCESS, str(completed)


def extract_examples():
    utila.log('extract examples')
    if os.path.exists(tests.resources.GENERATED):
        return
    os.makedirs(tests.resources.GENERATED)

    todo = os.path.join(tests.resources.GENERATED, 'todo')
    os.makedirs(todo)

    create_example(tests.resources.MASTER72)
    create_example(tests.resources.MASTER78)
    create_example(tests.resources.MASTER83)
    create_example(tests.resources.MASTER89)
    create_example(tests.resources.MASTER116)

    create_example(tests.resources.HOWTOWRITE9)
    create_example(tests.resources.ORDER38)

    create_example(
        tests.resources.PORTING_EXTENTION,
        todoname=tests.resources.EXAMPLE_JOB,
        filename='howto-cporting.pdf',  # TODO: decide what is correct, see below
    )
    create_example(
        tests.resources.RESTRUCTURED,
        todoname='2324123123',
        filename='The RestructuredText Book',
    )

    generate_broken_example()


def create_example(source: str, todoname: str = None, filename: str = None):
    todopath = os.path.join(tests.resources.GENERATED, 'todo')

    if todoname is None:
        todoname = os.path.basename(source)
        todoname = todoname.split('.')[0]  # remove file extention

    if filename is None:
        filename = 'sample.pdf'

    link.create_todo(
        source,
        filename=filename,
        todopath=todopath,
        todoname=todoname,
    )


def generate_broken_example():
    broken = utila.tmpfile(configo.tmp())
    utila.file_replace(broken, 'invalid pdf data')
    create_example(broken, todoname='broken_resource', filename='broken.pdf')
