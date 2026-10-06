# Docker Projects

Small sample apps, each with a Dockerfile to containerize it.

| Project | Stack | Container port | Folder |
|---|---|---|---|
| Flask app | Python 3.11, Flask 3.1.1 | 80 | [flask-app-containerization/](flask-app-containerization/) |
| React app | Node 20, React 18, Vite 5 | 5173 | [react-app-containerization/](react-app-containerization/) |

## 1. flask-app-containerization

A small Flask web app.

**Routes**
- `/` renders `templates/index.html`
- `/health` returns `Server is up and running`

**Files**
- `app.py`: the Flask routes
- `run.py`: starts the app on `0.0.0.0:80`
- `requirements.txt`: Python dependencies
- `Dockerfile`: builds the image on `python:3.11`, installs the requirements and runs `run.py`

**Build the image**
```bash
cd flask-app-containerization
docker build -t flask-app .
```

**Run the container**
```bash
docker run -d -p 5000:80 --name flask-app flask-app
# open http://localhost:5000
# health check: curl http://localhost:5000/health
```

**Useful commands**
```bash
docker logs -f flask-app          # follow the logs
docker exec -it flask-app bash    # open a shell inside the container
docker stop flask-app && docker rm flask-app
```

## 2. react-app-containerization

A small React checklist app built with Vite.

**Files**
- `src/`: the React components (`App.jsx`, `main.jsx`) and styles
- `package.json`: the `dev`, `build` and `preview` scripts
- `Dockerfile`: builds the image on `node:20-alpine`, installs dependencies and runs `npm run dev`

**Run locally without Docker**
```bash
cd react-app-containerization
npm install
npm run dev        # http://localhost:5173
```

**Build the image**
```bash
cd react-app-containerization
docker build -t react-docker-app .
```

**Run the container**
```bash
docker run -d -p 3000:5173 --name react-app react-docker-app
# open http://localhost:3000
```

**Useful commands**
```bash
docker logs -f react-app          # follow the logs
docker images react-docker-app    # show the image
docker exec -it react-app sh      # open a shell (Alpine image has sh, not bash)
docker stop react-app && docker rm react-app
```

## Notes

- The container port is the one the app listens on inside the container. The first number in `-p host:container` is the port you open on your machine.
- The React image runs Vite's development server, which is not meant for production.
- Both Dockerfiles have no `EXPOSE` line, so the `-p` flag is required to reach the apps.
