# Docker image for reproducible test runs
# Build:  docker build -t russia-tv-tests .
# Run:    docker run --rm -v $(pwd)/reports:/app/reports russia-tv-tests
# Compose: docker compose up --abort-on-container-exit

FROM python:3.12-slim-bookworm

# Install system deps: Node.js (for axe-core), curl, git
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git nodejs npm \
    # Playwright browser deps
    libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock package*.json ./
RUN uv sync --extra dev && uv run playwright install chromium
RUN npm ci

# Copy project files
COPY . .

# Default: run smoke E2E tests
CMD ["uv", "run", "pytest", "tests/e2e/", "-m", "smoke", "-v", "--alluredir=reports/allure-results"]
