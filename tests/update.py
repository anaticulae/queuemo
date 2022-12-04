# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import link
import power
import utila

import tests.resources

# TODO: REFACTOR TEST DATA GENERATOR


def extract_examples(files):
    todo = os.path.join(power.generated(), 'todo')
    if os.path.exists(todo):
        return
    os.makedirs(todo)

    for item in files:
        create_example(item)

    create_example(
        power.DOCU009_PDF,
        todoname=tests.resources.EXAMPLE_JOB,
        filename='howto-cporting.pdf',  # TODO: decide what is correct, see below
    )
    create_example(
        power.DOCU027_PDF,
        todoname='2324123123',
        filename='The RestructuredText Book',
    )

    generate_broken_example()


def create_example(source: str, todoname: str = None, filename: str = None):
    todopath = tests.resources.TODO

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
    tmpdir = configo.tmp()
    os.makedirs(tmpdir, exist_ok=True)
    broken = utila.tmpfile(tmpdir)
    utila.file_replace(broken, 'invalid pdf data')
    create_example(broken, todoname='broken_resource', filename='broken.pdf')
