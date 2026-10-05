# react-docker-app

A small React (Vite) checklist app, ready to containerize with a single-stage Dockerfile.

## Run locally (without Docker)
    npm install
    npm run dev          # http://localhost:5173

## Run with Docker
    docker build -t react-docker-app .
    docker run -d -p 3000:5173 --name react-app react-docker-app
    # open http://localhost:3000

## Useful commands
    docker logs -f react-app
    docker images react-docker-app
    docker exec -it react-app sh
    docker stop react-app && docker rm react-app
