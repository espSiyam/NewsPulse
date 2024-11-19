#!/bin/bash

echo "Pulling latest changes..."
git pull

echo "Building new Docker image..."
docker build -t news_api .

echo "Stopping and removing the old container..."
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)

echo "Running the new Docker container..."
docker run -d -p 8000:8000 --name news_api news_api
