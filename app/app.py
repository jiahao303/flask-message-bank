from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)

def get_message_db():
    if "message_db" not in g:
        g.message_db = sqlite3.connect("messages_db.sqlite")
    cursor = g.message_db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messages(id INT, handle TEXT, message TEXT)")
    return g.message_db

def insert_message(request):
    message = request.form["message"]
    handle = request.form["handle"]
    cursor = get_message_db().cursor()
    cursor.execute("SELECT COUNT(*) FROM messages")
    number_of_rows = cursor.fetchone()
    cursor.execute("INSERT INTO messages(id, handle, message) VALUES(" + str(number_of_rows[0] + 1) + ", \"" + handle + "\", \"" + message + "\")")
    get_message_db().commit()
    get_message_db().close()

def random_messages(n):
    cursor = get_message_db().cursor()
    cursor.execute("SELECT * FROM messages ORDER BY RANDOM() LIMIT " + str(n))
    random_messages = cursor.fetchall()
    print(random_messages)
    get_message_db().close()
    return random_messages

@app.route("/")
def main():
    return render_template("base.html")

@app.route("/submit/", methods = ["POST", "GET"])
def submit():
    if request.method == "GET":
        return render_template("submit.html")
    else:
        try:
            insert_message(request)
            return render_template("submit.html", thanks = True)
        except:
            return render_template("submit.html")

@app.route("/view/")
def view():
    return render_template("view.html", random_messages = random_messages(5))
