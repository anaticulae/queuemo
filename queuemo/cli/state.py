# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import argparse
import sys

import configos
import link
import utilo


@utilo.saveme
def main() -> int:
    action = eval_cli()
    if action.kill:
        kill(action.kill)
        return utilo.SUCCESS
    utilo.log('verify state ...')
    utilo.log(f'    todo: {configos.todo()}')
    print_running()
    print_waiting()
    return utilo.SUCCESS


def print_running():
    print_documents(link.State.RUNNING)


def print_waiting():
    print_documents(link.State.WAITING)


def print_documents(state):
    # TODO: PASS READY AND TODO TO AVOID REQUIRED COMMON PARENT
    common = utilo.path_parent(configos.ready())
    documents = link.load_documents(
        common=common,
        owner=None,
        state=state,
    )
    if not documents:
        utilo.log(f'no {state.name} documents')
        return
    utilo.log(f'\n{state.name} documents({len(documents)}):')
    for document in documents:
        print_document(document)


def print_document(document):
    pages = str(document.get('pages')).zfill(3)
    title = document.get('title')
    date = document.get('date')
    name = document.get('name')
    utilo.log(f'   - {name} {date} {pages} {title}')


def kill(documentid: str):
    if documentid == 'all':
        todos = collect_all()
        if not todos:
            utilo.error('nothing to kill')
            sys.exit(utilo.INVALID_COMMAND)
        for jobinfo in todos:
            kill(jobinfo.name)
        return
    if not link.document(documentid=documentid):
        utilo.error(f'invalid documentid: {documentid}')
        sys.exit(utilo.INVALID_COMMAND)
        return
    if link.deleted(documentid):
        utilo.error(f'already deleted: {documentid}')
        sys.exit(utilo.INVALID_COMMAND)
        return
    if link.delete(documentid):
        utilo.log(f'killed: {documentid}')
        return
    utilo.error(f'could not kill: {documentid}')
    sys.exit(utilo.INVALID_COMMAND)


def collect_all() -> list:
    todos = link.collect_jobs()[0]
    result = []
    for todo in todos:
        process = link.current(todo.documentid)
        current: link.State = link.State.fromstate(process)
        if current not in (link.State.WAITING, link.State.RUNNING):
            continue
        result.append(todo)
    return result


def eval_cli():
    parser = argparse.ArgumentParser(prog='queuemo_state',)
    parser.add_argument(
        '--kill',
        nargs='?',
        help='stop single job, use all to stop all pending jobs',
    )
    result = parser.parse_args()
    return result
