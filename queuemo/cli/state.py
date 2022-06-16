# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import argparse
import sys

import configo
import link
import utila


@utila.saveme
def main() -> int:
    action = eval_cli()
    if action.kill:
        kill(action.kill)
        return utila.SUCCESS
    utila.log('verify state ...')
    utila.log(f'    todo: {configo.todo()}')
    print_running()
    print_waiting()
    return utila.SUCCESS


def print_running():
    print_documents(link.State.RUNNING)


def print_waiting():
    print_documents(link.State.WAITING)


def print_documents(state):
    documents = link.load_documents(
        common=configo.share(),
        owner=None,
        state=state,
    )
    if not documents:
        utila.log(f'no {state.name} documents')
        return
    utila.log(f'\n{state.name} documents({len(documents)}):')
    for document in documents:
        print_document(document)


def print_document(document):
    pages = str(document.get('pages')).zfill(3)
    title = document.get('title')
    date = document.get('date')
    name = document.get('name')
    utila.log(f'   - {name} {date} {pages} {title}')


def kill(documentid: str):
    if not link.document(documentid=documentid):
        utila.error(f'invalid documentid: {documentid}')
        sys.exit(utila.INVALID_COMMAND)
        return
    if link.deleted(documentid):
        utila.error(f'already deleted: {documentid}')
        sys.exit(utila.INVALID_COMMAND)
        return
    if link.delete(documentid):
        utila.log(f'killed: {documentid}')
        return
    utila.error(f'could not kill: {documentid}')
    sys.exit(utila.INVALID_COMMAND)


def eval_cli():
    parser = argparse.ArgumentParser(prog='queuemo_state',)
    parser.add_argument('--kill', nargs='?', help='stop single job')
    result = parser.parse_args()
    return result
