
from SQLinint import db

def main():
    flights = db.execute("SELECT origin, destination, duration FROM flights").fetchall()

    # print(f"type :: {type(flights)}, {type(flights[0])}")
    for flight in flights:
        print(f"{flight.origin} to {flight.destination}, {flight.duration} minutes.")

if __name__ == "__main__":
    main()
