# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import utila

import tests.update

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

if not 'PYTEST_XDIST_WORKER' in os.environ:
    # master process only
    # ensure to avoid race condition if more than one thread tries to
    # install or use rawmaker

    if 'GENERATE' in os.environ or utila.test.LONGRUN:
        utila.log('install requirements')
        tests.update.install_requirements()
