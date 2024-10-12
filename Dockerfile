# Dockerfile
FROM python:3.12-slim-bullseye

# Create a non-root user
RUN useradd -m appuser

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip and install the Python dependencies
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

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