from flask import Flask, render_template, request, session
from flask_session import Session # does NOT comes with flask by default
# from flask.ext.session import Session
from SQLinint import db



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

@app.route("/flights")
def index_p():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index_p.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name").strip()
    if name == '':
        return render_template("error_p.html", message="Empty name not allowed !!")
    try:
        flight_id = int(request.form.get("flight_id"))
    except:
        return  render_template("error_p.html", message="Invalid flight ID(DO NOT TEMPER WITH HTML) !!!")
    if db.execute("SELECT * FROM flights WHERE id=:id",
                  {"id":flight_id}).rowcount==0:
        return render_template("error_p.html", message="No such flight exist !!!")

    db.execute("INSERT INTO passengers(name, flight_id) VALUES (:name, :flight_id)",
               {"name": name, "flight_id": flight_id})
    db.commit(); # no change commited untill this command execute...
    return render_template("success_p.html")

@app.route("/passengers")
def passengers():
    passengers_list = db.execute("SELECT * FROM passengers JOIN flights ON\
                                 flights.id=passengers.flight_id").fetchall()
    # for passenger in passengers_list:
    #     print(passenger)
    #     print(passenger.name)
    #     print(passenger.origin)
    #     print(passenger.destination)
    return render_template("passengers_list.html", passengers_list=passengers_list)

@app.route("/flight/<int:flight_id>")
def flight(flight_id):
    flight = db.execute("SELECT * FROM flights WHERE id=:id", {"id":flight_id}).fetchone()
    if flight is None:
        return render_template("error_p.html", message="No such flight exist !!!")
    passengers = db.execute("SELECT name from passengers WHERE flight_id=:flight_id", {"flight_id":flight_id})
    return render_template("passenger_in_flight.html", flight=flight, passengers=passengers)


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