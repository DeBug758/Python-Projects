#!/bin/bash

# Build Docker image with Flask app name
docker build -t flask-app .

# Check if the build was successful
if [ $? -eq 0 ]; then
  echo "Docker image build successful"
else
  echo "Error: Docker image build failed"
  exit 1
fi
