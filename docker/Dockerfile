FROM python:3.12-slim as builder_image
#Create an working directory and switch to it
WORKDIR /app

# Do not buffer python logs, output them directly
# Do not create .pyc files
# Do not cache pip packages
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"


FROM python:3.12-slim as runtime_image

ARG APP_DIRECTORY="/app"
ARG RUNTIME_USER="oss-user"

# Create an working directory and switch to it
WORKDIR ${APP_DIRECTORY}

# Do not buffer python logs, output them directly
# Do not create .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \

# Create a group with the name of the user
# Create the user and add it to the group with its own name
# Change the owner of the folder to the created user and group
# Change the permissions to read and execute only for the user and the group
RUN groupadd -r ${RUNTIME_USER} &&  \
    useradd -r -g ${RUNTIME_USER} ${RUNTIME_USER} && \
    chown -R ${RUNTIME_USER}:${RUNTIME_USER} $APPDIR && \
    chmod 550 -R $APPDIR

# Switch user context to the newly created user
USER ${RUNTIME_USER}

# Launch the application