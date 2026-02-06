
FROM ghcr.io/astral-sh/uv:latest AS uv

FROM python:3.13-slim

WORKDIR /app

# Copy uv binary
COPY --from=uv /uv /uvx /bin/

# Enable bytecode compilation (optional, slightly faster startup)
ENV UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./

# Install dependencies strictly from the lockfile
RUN uv sync --frozen --no-dev --no-install-project

# IMPORTANT: Add the created virtual environment to the PATH
ENV PATH="/app/.venv/bin:$PATH"

COPY main.py .
COPY ./models /app/models

## Run the app (no need to specify paths, it uses the PATH env var)
CMD ["fastapi", "run", "main.py", "--port", "8000",  "--proxy-headers"]
