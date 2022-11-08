#!/usr/bin/bash
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

CURRENT=$(queuemo --version)
RELEASE_TAG="${CAELUM_DOCKER_TEST}/caelum_release_work:${CURRENT}"
docker build -t $RELEASE_TAG --file Production .
