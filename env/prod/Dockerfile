# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

FROM python:3.15-slim

ENV PYTHONOPTIMIZE=2
# Makes application logs appear immediately in Docker logs.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install OpenGL
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Worker
COPY env/prod/entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

WORKDIR /app

COPY pyproject.toml README LICENSE ./
# Install dependencies
RUN pip install --no-cache-dir .

# Copy app
COPY queuemo/ ./queuemo
RUN pip install --no-cache-dir .

# Persistent data
VOLUME ["/data"]

# Application defaults
ENV SHARED_TODO=/data/shared/todo
ENV SHARED_READY=/data/shared/ready
ENV SHARED_SPACE=/data/shared/
ENV SHARED_TMP=/tmp

ENV JOBS=1200
ENV RUNTIME=1000000
ENV WORKER=16

ENTRYPOINT ["docker-entrypoint.sh"]
