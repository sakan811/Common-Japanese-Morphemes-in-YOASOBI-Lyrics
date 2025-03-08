# End-to-End Testing

This directory contains scripts and configuration for running end-to-end tests of the Japanese morphemes extractor application.

## Prerequisites

- Docker
- Docker Compose

## Running the Tests

### On Linux/macOS/Git Bash (Windows)

```bash
# Make the script executable (only needed once)
chmod +x run_test.sh

# Run the test
./run_test.sh
```

### On Windows PowerShell

```powershell
# Run the test
.\run_test.ps1
```

## What the Test Does

1. Builds the Docker image for the morphemes-extractor application
2. Creates a Docker network for communication between containers
3. Starts a PostgreSQL database container
4. Starts the morphemes-extractor container
5. Executes the main.py script inside the container
6. Monitors the logs and waits for completion
7. Reports the test result
8. Offers to clean up containers and volumes

## Configuration

The test environment is configured in the `docker-compose.yml` file. Key settings include:

- PostgreSQL database running on port 6000
- Volume mapping for the lyrics directory
- Environment variables for database connection
- Network configuration for inter-container communication

## Troubleshooting

If you encounter issues with path conversion on Windows, the scripts include automatic detection and handling of Windows environments to prevent path conversion problems.

If you need to modify the test configuration, edit the `docker-compose.yml` file. 