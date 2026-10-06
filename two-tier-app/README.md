# two-tier-app

Flask (web tier) + MySQL (database tier). A simple guestbook.
No Dockerfile included on purpose, write your own.

## Files
    app.py             Flask app (reads DB settings from environment variables)
    requirements.txt   Flask, PyMySQL, cryptography
    templates/index.html

## Environment variables
| Variable      | Default   | Meaning                  |
|---------------|-----------|--------------------------|
| DB_HOST       | localhost | database hostname        |
| DB_PORT       | 3306      | database port            |
| DB_USER       | appuser   | database user            |
| DB_PASSWORD   | apppass   | database password        |
| DB_NAME       | appdb     | database name            |
| PORT          | 5000      | port Flask listens on    |

## Routes
    /               guestbook page
    /add            POST, save a message
    /delete/<id>    POST, delete a message
    /api/messages   all messages as JSON
    /health         200 if the database is reachable, 503 if not

## Hints for your Dockerfile
- App listens on 0.0.0.0, port 5000 (change with PORT)
- Start command: python app.py
- The app creates the table itself and retries until MySQL is ready

## Running the containers (after you write the Dockerfile)
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

Open http://localhost:5000
