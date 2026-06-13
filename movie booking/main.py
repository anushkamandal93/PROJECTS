import json
from pathlib import Path

class MovieBooking:

    database = "movies.json"
    data = []

    if Path(database).exists():
        with open(database) as Myfile:
            data = json.loads(Myfile.read())

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as Myfile:
            Myfile.write(json.dumps(cls.data))

    def add_movie(self):
        movie = {
            "movie_name": input("Enter movie name: "),
            "available_seats": int(input("Enter total seats: "))
        }

        MovieBooking.data.append(movie)
        MovieBooking.__update()

        print("Movie added successfully!")

    def book_ticket(self):

        movie_name = input("Enter movie name: ")

        movie = [
            i for i in MovieBooking.data
            if i["movie_name"].lower() == movie_name.lower()
        ]

        if not movie:
            print("Movie not found")
            return

        seats = int(input("How many seats do you want? "))

        if seats > movie[0]["available_seats"]:
            print("Seats not available")
        else:
            movie[0]["available_seats"] -= seats

            MovieBooking.__update()

            print(f"{seats} ticket(s) booked successfully")

    def cancel_ticket(self):

        movie_name = input("Enter movie name: ")

        movie = [
            i for i in MovieBooking.data
            if i["movie_name"].lower() == movie_name.lower()
        ]

        if not movie:
            print("Movie not found")
            return

        seats = int(input("How many tickets cancel? "))

        movie[0]["available_seats"] += seats

        MovieBooking.__update()

        print("Ticket cancelled successfully")

    def show_movies(self):

        for movie in MovieBooking.data:
            print("\nMovie:", movie["movie_name"])
            print("Available Seats:", movie["available_seats"])

booking = MovieBooking()

print("1. Add Movie")
print("2. Book Ticket")
print("3. Cancel Ticket")
print("4. Show Movies")

choice = int(input("Enter your choice: "))

if choice == 1:
    booking.add_movie()

elif choice == 2:
    booking.book_ticket()

elif choice == 3:
    booking.cancel_ticket()

elif choice == 4:
    booking.show_movies()