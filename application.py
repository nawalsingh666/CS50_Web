from flask import Flask, render_template, request, session
from flask_session import Session # does NOT comes with flask by default

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

global_notes = []


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global_notes.append(request.form.get('note'))
    print(global_notes)
    return render_template("global_chat.html", notes=global_notes)


@app.route("/private", methods = ['GET', 'POST'])
def private():
    if request.method == 'POST':
        if session.get("notes") is None:
            session["notes"] = None;
        session["notes"].append(request.form.get("note"))
    return render_template("global_chat.html", notes=session["notes"])


# Error handling, ....................................
@app.errorhandler(404)
def error_404(e):
    # print(e)
    return render_template("error_404.html"), 404


app.register_error_handler(404, error_404)

