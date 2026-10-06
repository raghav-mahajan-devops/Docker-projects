import os
import socket
import time

import pymysql
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

# Database settings come from environment variables, so the same code
# works on your laptop and inside containers.
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")
DB_NAME = os.getenv("DB_NAME", "appdb")
PORT = int(os.getenv("PORT", "5000"))


def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
        connect_timeout=5,
    )


def init_db(retries=30, delay=2):
    """Create the table. Retries because the DB container may start slower than the app."""
    for attempt in range(1, retries + 1):
        try:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS messages (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(80) NOT NULL,
                        message VARCHAR(500) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
            conn.close()
            print("Database ready", flush=True)
            return
        except pymysql.MySQLError as err:
            print(f"Waiting for database ({attempt}/{retries}): {err}", flush=True)
            time.sleep(delay)
    raise RuntimeError("Could not connect to the database")


@app.route("/")
def index():
    messages, error = [], None
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, message, created_at FROM messages ORDER BY id DESC")
            messages = cur.fetchall()
        conn.close()
    except pymysql.MySQLError as err:
        error = str(err)
    return render_template(
        "index.html",
        messages=messages,
        error=error,
        web_host=socket.gethostname(),
        db_host=DB_HOST,
    )


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name", "").strip()[:80]
    message = request.form.get("message", "").strip()[:500]
    if name and message:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO messages (name, message) VALUES (%s, %s)", (name, message))
        conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:msg_id>", methods=["POST"])
def delete(msg_id):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM messages WHERE id = %s", (msg_id,))
    conn.close()
    return redirect(url_for("index"))


@app.route("/api/messages")
def api_messages():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, message, created_at FROM messages ORDER BY id DESC")
        rows = cur.fetchall()
    conn.close()
    for r in rows:
        r["created_at"] = r["created_at"].isoformat()
    return jsonify(rows)


@app.route("/health")
def health():
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
        conn.close()
        return jsonify(status="ok", database="connected"), 200
    except pymysql.MySQLError as err:
        return jsonify(status="error", database=str(err)), 503


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=PORT)
