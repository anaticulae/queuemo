# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http
import threading
import urllib.error
import urllib.request

import flask
import utilo

import queuemo.recipes.logger
import queuemo.runtime.status

app = flask.Flask(__name__)

STATUS = """
<pre>
THIS IS A QUEUEMO WORKER

RUNNING: %s
</pre>
"""


@app.route('/')
def welcome():
    running = queuemo.runtime.status.isrunning()
    status = STATUS % running
    return status


@app.route('/log')
def show_log():
    current = queuemo.recipes.logger.complete()
    result = f'<pre>{current}</pre>'
    return result


@app.route('/current')
def show_current():
    current = queuemo.recipes.logger.content()
    result = f'<pre>{current}</pre>'
    return result


@app.route('/stop')
def stop():
    if queuemo.runtime.status.isstoped():
        return 'ALREADY STOPPED', http.HTTPStatus.FORBIDDEN
    queuemo.runtime.status.stop()
    return 'STOPPED'


def start():
    port = freeport()
    utilo.log(f'start http interface on port: {port}')
    runtime = threading.Thread(
        target=app.run,
        kwargs={'port': port},
        daemon=True,
    )
    runtime.start()
    return runtime


def freeport(firstport: int = 7000) -> int:
    for port in range(50):
        port = firstport + port
        url = f'http://localhost:{port}'
        try:
            with urllib.request.urlopen(url, timeout=1) as request:  # nosec
                if request.read():
                    continue
        except urllib.error.URLError:
            return port
    return None
