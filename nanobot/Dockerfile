# Adapted from backend/Dockerfile and qwen-code-api/Dockerfile
# Also see https://docs.astral.sh/uv/guides/integration/docker/

# ---
# Stage 1: build the application in the `/app` directory.
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Disable Python downloads - use the system interpreter across both images.
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy workspace root pyproject.toml and uv.lock for dependency resolution
COPY --from=workspace pyproject.toml uv.lock /app/

# Copy mcp-lms for workspace dependency resolution (needed for uv sync)
COPY --from=mcp mcp-lms /app/mcp/mcp-lms

# Copy nanobot-websocket-channel for workspace dependency resolution
COPY --from=webchat . /app/nanobot-websocket-channel

# Copy nanobot project files
COPY pyproject.toml /app/nanobot/pyproject.toml

# Sync dependencies for nanobot package
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package nanobot

# Copy the rest of nanobot source
COPY . /app/nanobot

# Sync again to install the nanobot package itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot

# ---
# Stage 2: use a final image without uv
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

# Set environment variables for Python and application
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Make sure we use UTF-8 encoding
ENV LANG=C.UTF-8

# Accept build args for UID/GID
ARG APP_UID=1000
ARG APP_GID=1000

# Setup a non-root user with configurable UID/GID
RUN groupadd --system --gid ${APP_GID} appuser \
    && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home appuser

# Copy the application from the builder
COPY --from=builder --chown=${APP_UID}:${APP_GID} /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Use the non-root user to run our application
USER ${APP_UID}:${APP_GID}

# Use `/app/nanobot` as the working directory
WORKDIR /app/nanobot

# Run the entrypoint script
CMD ["python", "/app/nanobot/entrypoint.py"]
