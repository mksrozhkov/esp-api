FROM python:3.11-slim AS python-base

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.7.1 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base AS builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev

# `production` image used for runtime
FROM python-base AS production
ENV ENVIRONMENT=prod
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY . ./
