FROM python:3.13-slim

# ---- System dependencies for OpenCV / PaddleOCR ----
# libgl1, libglib2.0-0: required by cv2 (headless envs don't have these by default)
# libgomp1: OpenMP runtime needed by paddlepaddle
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# ---- Install uv ----
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# ---- Dependency layer (cached separately from source code) ----
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# ---- Application source ----
COPY . .

# Install the project itself now that source is present
RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]