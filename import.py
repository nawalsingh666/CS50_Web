import csv
import os

from flask import Flask

# from SQLinint import  # old SQL model type
from models import db, Flight, Passenger

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://nawal:handeercel@localhost/database_1'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("flights.csv")
    reader = csv.reader(f)
    for origin, destination, duration in reader:
    #     db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :destination, :duration)",
    #                 {"origin": origin, "destination": destination, "duration": duration})
    #     print(f"Added flight from {origin} to {destination} lasting {duration} minutes.")
    # db.commit()
        flight = Flight(origin=origin, destination=destination, duration=duration)
        db.session.add(flight)
        print(f"Added flight from {origin} to {destination} lasting {duration} minutes.")
    db.session.commit()
if __name__ == "__main__":
    with app.app_context():
        main()
