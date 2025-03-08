#!/bin/bash
set -e

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting end-to-end test execution...${NC}"

# Detect OS for platform-specific settings
OS_TYPE="$(uname -s)"
case "${OS_TYPE}" in
    CYGWIN*|MINGW*|MSYS*)
        echo -e "${YELLOW}Detected Windows environment...${NC}"
        # Set path conversion prevention for Windows Git Bash/MSYS
        export MSYS_NO_PATHCONV=1
        ;;
    Darwin*)
        echo -e "${YELLOW}Detected macOS environment...${NC}"
        ;;
    Linux*)
        echo -e "${YELLOW}Detected Linux environment...${NC}"
        ;;
    *)
        echo -e "${YELLOW}Unknown OS: ${OS_TYPE}, proceeding with default settings...${NC}"
        ;;
esac

# Change to the e2e_test directory
cd "$(dirname "$0")"

echo -e "${YELLOW}Building and starting containers...${NC}"
docker-compose up --build -d

echo -e "${YELLOW}Containers started. Checking logs...${NC}"
docker-compose logs

# Execute the Python script in the morphemes-extractor container
echo -e "${YELLOW}Running main.py in morphemes-extractor container...${NC}"
docker exec morphemes-extractor python main.py
EXIT_CODE=$?

if [ "$EXIT_CODE" -eq 0 ]; then
    echo -e "${GREEN}End-to-end test completed successfully!${NC}"
else
    echo -e "\033[0;31mEnd-to-end test failed with exit code $EXIT_CODE\033[0m"
fi

# Ask if user wants to clean up
read -p "Do you want to clean up containers and volumes? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Cleaning up containers and volumes...${NC}"
    docker-compose down -v
else
    echo -e "${YELLOW}Stopping containers but keeping volumes...${NC}"
    docker-compose down
fi

exit $EXIT_CODE 