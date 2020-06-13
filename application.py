from flask import Flask, render_template, request, session
from flask_session import Session # does NOT comes with flask by default
# from flask.ext.session import Session
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# app.secret_key = "Top Secret !!!"

global_notes = []


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global_notes.append(request.form.get('note'))
    heading = "GLOBAL NOTES"
    return render_template("global_notes.html", notes=global_notes, heading_name=heading)


@app.route("/private", methods = ['GET', 'POST'])
def private():
    # print("full", session)
    if session.get("notes") is None:
        session["notes"] = []
    if request.method == 'POST':
        session["notes"].append(request.form.get("note"))
    heading = "LOCAL NOTES"
    return render_template("global_notes.html", notes=session["notes"], heading_name=heading)


# Error handling, ....................................
@app.errorhandler(404)
def error_404(e):
    # print(e)
    return render_template("error_404.html"), 404


app.register_error_handler(404, error_404)


# run it !!!
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=2010, threaded=True)