FROM python:3.10-slim

WORKDIR /app

# System deps (Playwright will install additional deps via --with-deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install browsers + OS deps
RUN python -m playwright install --with-deps chromium

COPY . /app

CMD ["pytest"]
