# Dockerfile
# Build stage
FROM python:3.13-slim-bullseye AS builder

# Copy UV from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install build dependencies, install dependencies, and clean up in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    && uv pip install --system --upgrade pip \
    && uv pip install --system -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Final stage
FROM python:3.13-slim-bullseye

# Copy UV from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create a non-root user
RUN useradd -m appuser

# Set the working directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Install unidic directly in the final stage
RUN python -m unidic download

# Copy application code
COPY . .

# Change ownership of the application files to appuser
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Keep the container running
CMD ["tail", "-f", "/dev/null"]