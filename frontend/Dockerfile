FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# ---- Dependency layer ----
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# ---- Application source ----
COPY . .

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "streamlit_app.py", \
     "--server.address=0.0.0.0", "--server.port=8501"]