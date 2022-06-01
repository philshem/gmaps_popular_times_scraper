#!/bin/bash
set -e

docker-compose build
docker-compose up -d

docker exec -it gmaps-scraper bash