#Set global variables that can be inherited inside the stages
ARG APP_NAME="openshootingsolutions-remote"
ARG APP_DIR="/app/oss/${APP_NAME}"

FROM python:3.12-slim as builder_image
# Inherit the global variables APP_NAME and APP_DIR
ARG APP_NAME
ARG APP_DIR

#Create an working directory and switch to it
WORKDIR ${APP_DIR}

# Do not buffer python logs, output them directly
# Do not create .pyc files
# Disable PIP version checks
# Do not cache pip packages
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1


# Set VIRTUAL_ENV which is used by third party tools to detect the use of a virtual environment
ENV VIRTUAL_ENV="${APP_DIR}/.venv"

# Create the VENV and add it to the path variable
RUN python3 -m venv $VIRTUAL_ENV

# Now add the path to the PATH variable
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

# RUN pip to install the package
RUN pip install ${APP_NAME}

FROM python:3.12-slim as runtime_image
# Inherit the global variables APP_NAME and APP_DIR
ARG APP_NAME
ARG APP_DIR

# Create an working directory and switch to it
WORKDIR ${APP_DIR}

# Do not buffer python logs, output them directly
# Do not create .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set VIRTUAL_ENV which is used by third party tools to detect the use of a virtual environment
ENV VIRTUAL_ENV="${APP_DIR}/.venv"

# Now add the path to the PATH variable
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

# COPY the VENV from the builder stage
COPY --from=builder_image ${APP_DIR} ${APP_DIR}

# Create a group with the name of the user
# Create the user and add it to the group with its own name
# Change the owner of the folder to the created user and group
# Change the permissions to read and execute only for the user and the group
ENV RUNTIME_USER="oss-user"
RUN groupadd -r "${RUNTIME_USER}" &&  \
    useradd -r -g "${RUNTIME_USER}" "${RUNTIME_USER}" && \
    chown -R "${RUNTIME_USER}:${RUNTIME_USER}" "${APP_DIR}" && \
    chmod 550 -R "${APP_DIR}"

# Switch user context to the newly created user
USER ${RUNTIME_USER}

# Launch the application
ENTRYPOINT ["oss-remote"]
