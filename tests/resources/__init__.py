# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import queuemo

RESOURCES = os.path.join(queuemo.ROOT, 'tests/resources')
assert os.path.exists(RESOURCES), RESOURCES

PDF = os.path.join(RESOURCES, 'pdf')

GENERATED = os.path.join(RESOURCES, 'generated')

TODO = os.path.join(GENERATED, 'todo')

EXAMPLE_JOB = '8166109011'
EXAMPLE_JOB_PATH = os.path.join(TODO, EXAMPLE_JOB)
EXAMPLE_PDF = os.path.join(EXAMPLE_JOB_PATH, EXAMPLE_JOB)

MASTER = os.path.join(PDF, 'master')
DOCU = os.path.join(PDF, 'docu')
ORDER = os.path.join(PDF, 'order')

GENERATED_TODO = os.path.join(GENERATED, 'todo')

MASTER72 = os.path.join(MASTER, 'page_72_noimages_toc.pdf')
MASTER78 = os.path.join(MASTER, 'page_78_images_toc.pdf')
MASTER83 = os.path.join(MASTER, 'page_83_noimages_toc.pdf')
MASTER89 = os.path.join(MASTER, 'page_89_noimages_toc.pdf')
MASTER116 = os.path.join(MASTER, 'page_116_images_toc_formular.pdf')

HOWTOWRITE9 = os.path.join(ORDER, 'howtowrite_pages9.pdf')
ORDER38 = os.path.join(ORDER, 'page_38.pdf')

PORTING_EXTENTION = os.path.join(DOCU, 'porting_extension_modules.pdf')
RESTRUCTURED = os.path.join(DOCU, 'restructuredtext.pdf')

MASTER72_JOB = os.path.join(GENERATED_TODO, 'page_72_noimages_toc')
PORTING_EXTENTION_JOB = os.path.join(GENERATED_TODO, EXAMPLE_JOB)
RESTRUCTURED_JOB = os.path.join(GENERATED_TODO, '2324123123')

REQUIRED_RESOURCES = [
    DOCU,
    EXAMPLE_JOB_PATH,
    EXAMPLE_PDF,
    HOWTOWRITE9,
    MASTER,
    MASTER116,
    MASTER72,
    MASTER72_JOB,
    MASTER78,
    MASTER83,
    MASTER89,
    ORDER,
    ORDER38,
    PORTING_EXTENTION,
    PORTING_EXTENTION_JOB,
    RESTRUCTURED,
    RESTRUCTURED_JOB,
    TODO,
]
