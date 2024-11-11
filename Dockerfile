# ================================
# Base Stage
# ================================

ARG PYTHON_VERSION
FROM python:3.11-bookworm AS base

# Arguments
ARG PORT=8000
EXPOSE ${PORT}

# Prerequisites
RUN rm -rf /var/lib/apt/lists/* & apt-get -y update && apt-get -y --no-install-recommends install python3 python3-pip

# Python
RUN pip install --upgrade pip

# uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.11 \
    UV_PROJECT_ENVIRONMENT=/app

# Copy energemin
COPY . ./energemin
WORKDIR /energemin

RUN --mount=type=cache,target=/root/.cache <<EOT
uv sync \
    --locked \
    --no-dev \
    --no-install-project
EOT

RUN --mount=type=cache,target=/root/.cache \
    uv pip install \
        --python=$UV_PROJECT_ENVIRONMENT \
        --no-deps \
        .

# ================================
# App Stage (used for the chainlit application)
# ================================
FROM base AS app

CMD exec make launch-ui