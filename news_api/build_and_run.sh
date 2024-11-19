#!/bin/bash

# Pull the latest changes
echo "Pulling latest changes..."
git pull

# Clean up old Docker containers, images, and volumes
echo "Cleaning up old Docker containers, images, and volumes..."
docker container prune -f  # Remove stopped containers
docker image prune -a -f  # Remove unused images
docker volume prune -f     # Remove unused volumes

# Build the new Docker image
echo "Building new Docker image..."
docker build -t news_api .

# Run the new Docker container
echo "Running the new Docker container..."
docker run -d -p 8000:8000 news_api
