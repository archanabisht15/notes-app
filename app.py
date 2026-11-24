import os
import time
import pymysql
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)


def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "password"),
        database=os.getenv("DB_NAME", "notesdb"),
        autocommit=True,
    )


def init_db():
    # Wait for the database to be ready (DB pod may start later)
    for _ in range(30):
        try:
            db = get_db()
            with db.cursor() as c:
                c.execute(
                    "CREATE TABLE IF NOT EXISTS notes ("
                    "id INT AUTO_INCREMENT PRIMARY KEY, "
                    "text VARCHAR(255) NOT NULL)"
                )
            db.close()
            print("Database ready")
            return
        except Exception as e:
            print("Waiting for database...", e)
            time.sleep(3)


PAGE = """
<!doctype html>
<title>My Notes</title>
<body style="font-family: Arial; max-width: 500px; margin: 40px auto;">
  <h2>sed -i 's/My Notes App/My Notes App v3/' app.py<h2>
  <form method="post">
    <input name="text" placeholder="Write a note" style="width:70%; padding:8px;" required>
    <button style="padding:8px;">Add</button>
  </form>
  <ul>
    {% for n in notes %}<li>{{ n[1] }}</li>{% endfor %}
  </ul>
</body>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    db = get_db()
    with db.cursor() as c:
        if request.method == "POST":
            text = request.form.get("text", "").strip()
            if text:
                c.execute("INSERT INTO notes (text) VALUES (%s)", (text,))
            db.close()
            return redirect("/")
        c.execute("SELECT id, text FROM notes ORDER BY id DESC")
        notes = c.fetchall()
    db.close()
    return render_template_string(PAGE, notes=notes)


@app.route("/health")
def health():
    return "ok"


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
