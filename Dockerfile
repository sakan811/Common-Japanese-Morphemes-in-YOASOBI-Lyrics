# Dockerfile
FROM python:3.13-slim-bullseye
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create a non-root user
RUN useradd -m appuser

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip and install the Python dependencies
RUN uv pip install --system --upgrade pip
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Download Unidic
RUN python -m unidic download

# Copy the rest of the application code
COPY . .

# Change ownership of the application files to appuser
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Keep the container running
CMD ["tail", "-f", "/dev/null"]