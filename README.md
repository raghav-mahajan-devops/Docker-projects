# Docker Projects

Small sample apps, each with a Dockerfile to containerize it.

| Project | Stack | Container port | Folder |
|---|---|---|---|
| Flask app | Python 3.11, Flask 3.1.1 | 80 | [flask-app-containerization/](flask-app-containerization/) |
| React app | Node 20, React 18, Vite 5 | 5173 | [react-app-containerization/](react-app-containerization/) |
| Two-tier app | Flask + MySQL 8, run with Docker Compose | 5000 | [two-tier-app/](two-tier-app/) |

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

## 3. two-tier-app

A guestbook app with two tiers: a Flask web tier and a MySQL 8 database tier. Users can leave, view and delete messages.

**Files**
- `app.py`: Flask routes. Reads the database settings from environment variables and creates the `messages` table on startup, retrying until MySQL is ready.
- `templates/index.html`: the guestbook page
- `requirements.txt`: Flask, PyMySQL, cryptography
- `Dockerfile`: multi-stage build on `python:3.11` (builder) and `python:3.11-slim` (runtime)
- `docker-compose.yml`: starts MySQL and the Flask app together on one network

**Environment variables** (defaults in `app.py`)

| Variable | Default | Meaning |
|---|---|---|
| `DB_HOST` | `localhost` | database hostname |
| `DB_PORT` | `3306` | database port |
| `DB_USER` | `appuser` | database user |
| `DB_PASSWORD` | `apppass` | database password |
| `DB_NAME` | `appdb` | database name |
| `PORT` | `5000` | port Flask listens on |

**Routes**

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | guestbook page |
| `/add` | POST | save a message |
| `/delete/<id>` | POST | delete a message |
| `/api/messages` | GET | all messages as JSON |
| `/health` | GET | `200` if the database is reachable, `503` if not |

**Run with Docker Compose (recommended)**
```bash
cd two-tier-app
docker compose up -d --build
# open http://localhost:5000
```

**Stop**
```bash
docker compose down        # stop and remove the containers
```

**Run with plain Docker** (alternative, without Compose)
```bash
docker network create two-tier

docker run -d --name mysql-db --network two-tier \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=appdb \
  -e MYSQL_USER=appuser \
  -e MYSQL_PASSWORD=apppass \
  -v mysql-data:/var/lib/mysql \
  mysql:8

docker build -t two-tier-app .

docker run -d --name web --network two-tier -p 5000:5000 \
  -e DB_HOST=mysql-db \
  two-tier-app
```

**Useful commands**
```bash
docker compose logs -f flask-app   # follow the web tier logs
docker compose ps                  # check container status
curl http://localhost:5000/health  # database connectivity check
```

## Notes

- The container port is the one the app listens on inside the container. The first number in `-p host:container` is the port you open on your machine.
- The React image runs Vite's development server, which is not meant for production.
- The flask-app and React Dockerfiles have no `EXPOSE` line, so the `-p` flag is required to reach the apps.
- The MySQL credentials in `docker-compose.yml` and `app.py` are sample values for local practice. Change them before using this anywhere else.
