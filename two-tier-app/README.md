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


Open http://localhost:5000
