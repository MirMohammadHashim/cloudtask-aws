import os

import mysql.connector
from flask import Flask, redirect, render_template, request

# Create the web app. Web pages come from the "frontend" folder.
app = Flask(__name__, template_folder="frontend")


def get_connection():
    # Open a line to the database. The address and password come from
    # settings given to the program, so they are never written in the code.
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database="cloudtask",
        connection_timeout=5,
    )


@app.route("/")
def home():
    # Someone opened the website: get all tasks and show the page.
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    # Someone clicked Add: save the new task, then show the page again.
    title = request.form["title"].strip()
    if title:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        conn.commit()
        conn.close()
    return redirect("/")


@app.route("/health")
def health():
    # The load balancer asks this: are you alive?
    return "ok"
