FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . .

RUN uv sync --locked --no-dev

CMD ["uv", "run", "python", "src/gerador_transacoes.py"]