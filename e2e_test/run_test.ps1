# PowerShell script for running end-to-end tests

# Define colors for output
$Green = [System.ConsoleColor]::Green
$Yellow = [System.ConsoleColor]::Yellow
$Red = [System.ConsoleColor]::Red

Write-Host "Starting end-to-end test execution..." -ForegroundColor $Green

# Change to the e2e_test directory
Set-Location -Path $PSScriptRoot

Write-Host "Building and starting containers..." -ForegroundColor $Yellow
docker-compose up --build -d

Write-Host "Containers started. Checking logs..." -ForegroundColor $Yellow
docker-compose logs

# Execute the Python script in the morphemes-extractor container
Write-Host "Running main.py in morphemes-extractor container..." -ForegroundColor $Yellow
docker exec morphemes-extractor python main.py
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "End-to-end test completed successfully!" -ForegroundColor $Green
} else {
    Write-Host "End-to-end test failed with exit code $exitCode" -ForegroundColor $Red
}

# Ask if user wants to clean up
$cleanup = Read-Host "Do you want to clean up containers and volumes? (y/n)"
if ($cleanup -eq "y" -or $cleanup -eq "Y") {
    Write-Host "Cleaning up containers and volumes..." -ForegroundColor $Yellow
    docker-compose down -v
} else {
    Write-Host "Stopping containers but keeping volumes..." -ForegroundColor $Yellow
    docker-compose down
}

exit $exitCode 