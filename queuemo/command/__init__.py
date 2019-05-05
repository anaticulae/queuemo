# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from configo import check_startup
from utila import SUCCESS
from utila import Command
from utila import create_parser
from utila import parse
from utila import saveme

from queuemo import __version__
from queuemo.worker.scheduler import run as start_scheduler


@saveme
def main():
    check_startup()
    start_scheduler()
    return SUCCESS
