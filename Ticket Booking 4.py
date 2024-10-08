import tkinter as tk
from tkinter import messagebox, PhotoImage

class MovieTicketBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Booking System")
        self.root.geometry("1500x2000")
        self.root.configure(bg="#f2f2f2")

        # Load images for each movie
        self.movie_images = {
            "Kalki 2898AD": PhotoImage(file="kalki.png"),
            "They Call Him OG": PhotoImage(file="og.png"),
            "Devara": PhotoImage(file="devara.png")
        }

        # Movie Data with Seat Pricing
        self.movies = {
            "Kalki 2898AD": {"showtimes": ["9:00 AM", "12:00 PM", "3:00 PM"], "price": {"Best": 250, "Average": 180, "Low Price": 120}},
            "They Call Him OG": {"showtimes": ["10:00 AM", "1:00 PM", "4:00 PM"], "price": {"Best": 250, "Average": 180, "Low Price": 120}},
            "Devara": {"showtimes": ["11:00 AM", "2:00 PM", "5:00 PM"], "price": {"Best": 250, "Average": 180, "Low Price": 120}},
        }

        self.selected_movie = None
        self.selected_showtime = None

        self.rows = 10
        self.columns = 20
        self.seat_buttons = {}
        self.booked_seats = []  # Seats booked for the current session

        # Store booked seats per movie and showtime
        self.booked_seats_by_show = {}  # Dictionary to store booked seats based on (movie, showtime)

        self.create_movie_selection_screen()

    def create_movie_selection_screen(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Movie Poster Selection Frame
        movie_frame = tk.Frame(self.root, bg="#e6e6e6")
        movie_frame.pack(pady=20)

        tk.Label(movie_frame, text="PVR INOX NOW SHOWING", font=("Arial", 14, "bold"), bg="#e6e6e6").pack(pady=10)

        # Create buttons for each movie with its poster
        for movie_name, image in self.movie_images.items():
            movie_button = tk.Button(movie_frame, image=image, command=lambda m=movie_name: self.proceed_to_showtime(m))
            movie_button.pack(side="left", padx=20)

    def proceed_to_showtime(self, movie_name):
        self.selected_movie = movie_name

        # Remove movie selection screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Showtime Selection
        self.showtime_frame = tk.Frame(self.root, bg="#e6e6e6", bd=2, relief=tk.RIDGE)
        self.showtime_frame.pack(pady=20)
        tk.Label(self.showtime_frame, text=f"Select Showtime for {self.selected_movie}:", font=("Arial", 12, "bold"), bg="#e6e6e6").pack(side="left", padx=10)

        self.showtime_var = tk.StringVar()
        showtimes = self.movies[self.selected_movie]["showtimes"]
        self.showtime_combo = tk.OptionMenu(self.showtime_frame, self.showtime_var, *showtimes)
        self.showtime_combo.config(font=("Arial", 10), width=15)
        self.showtime_combo.pack(side="left", padx=10)
        self.showtime_var.set(showtimes[0])

        # Button to proceed to seat selection
        self.select_seats_button = tk.Button(self.root, text="Select Seats", command=self.proceed_to_seat_selection, font=("Arial", 12), bg="#004d99", fg="white", width=20)
        self.select_seats_button.pack(pady=20)

    def proceed_to_seat_selection(self):
        self.selected_showtime = self.showtime_var.get()

        if not self.selected_showtime:
            messagebox.showwarning("Input Error", "Please select a showtime!")
            return

        # Hide previous UI elements
        self.showtime_frame.pack_forget()
        self.select_seats_button.pack_forget()

        # Move "Book Now" button to the top of the window
        self.book_button = tk.Button(self.root, text="Book Now", command=self.confirm_booking,
                                     font=("Arial", 14), bg="#004d99", fg="white", width=20)
        self.book_button.pack(pady=20)

        # Show Seat Grid based on seat zones
        self.create_seat_grid()

    def create_seat_grid(self):
        # Seat Grid Layout: 3 zones: Best, Average, and Low Price
        seat_zone = [
            ('Best', 'white', 4, 250),         # Best seats: 4 rows, 250 Rupees
            ('Average', 'white', 3, 180),     # Average seats: 3 rows, 180 Rupees
            ('Low Price', 'white', 3, 120)   # Low price seats: 3 rows, 120 Rupees
        ]

        self.seat_frame = tk.Frame(self.root, bg="#f2f2f2", bd=2, relief=tk.SUNKEN)
        self.seat_frame.pack(pady=20)

        self.booked_seats = []  # Reset booked seats for the current session

        # Get booked seats for the current movie and showtime
        current_show_key = (self.selected_movie, self.selected_showtime)
        if current_show_key not in self.booked_seats_by_show:
            self.booked_seats_by_show[current_show_key] = []

        booked_for_this_show = self.booked_seats_by_show[current_show_key]

        seat_num = 1
        row_offset = 0

        # Display labels for each class with pricing
        for zone, color, rows_in_zone, price in seat_zone:
            zone_label = tk.Label(self.seat_frame, text=f"{zone} Class (₹{price})", font=("Arial", 12, "bold"), bg="#f2f2f2")
            zone_label.grid(row=row_offset, column=0, columnspan=self.columns, pady=10)
            row_offset += 1

            for row in range(rows_in_zone):
                for column in range(self.columns):
                    # Check if the seat has already been booked for this show
                    if seat_num in booked_for_this_show:
                        seat_button = tk.Button(self.seat_frame, text=f"{seat_num}", width=4, height=1,  # Reduced width and height
                                                bg="grey", font=("Arial", 10), state="disabled")
                    else:
                        seat_button = tk.Button(self.seat_frame, text=f"{seat_num}", width=4, height=1,  # Reduced width and height
                                                bg=color, font=("Arial", 10),
                                                command=lambda num=seat_num, zone=zone: self.book_seat(num, zone))
                    seat_button.grid(row=row + row_offset, column=column, padx=2, pady=2)
                    self.seat_buttons[seat_num] = seat_button
                    seat_num += 1
            row_offset += rows_in_zone

    def book_seat(self, seat_num, zone):
        if seat_num in [seat[0] for seat in self.booked_seats]:
            # Deselect the seat
            self.booked_seats = [seat for seat in self.booked_seats if seat[0] != seat_num]
            self.seat_buttons[seat_num].config(bg="white")  # Reset to white color
        else:
            # Check if more than 6 seats are already booked
            if len(self.booked_seats) >= 6:
                messagebox.showwarning("Limit Reached", "You cannot book more than 6 seats at a time!")
                return

            # Select the seat
            self.seat_buttons[seat_num].config(bg="red")
            self.booked_seats.append((seat_num, zone))

    def confirm_booking(self):
        if not self.booked_seats:
            messagebox.showwarning("Booking Error", "No seats have been selected!")
            return

        total_price = 0
        booked_seat_details = []

        # Calculate total price based on the seat zone
        for seat_num, zone in self.booked_seats:
            price = self.movies[self.selected_movie]["price"][zone]
            total_price += price
            booked_seat_details.append(f"Seat {seat_num} ({zone})")

            # Mark the seat as booked for this movie and showtime
            current_show_key = (self.selected_movie, self.selected_showtime)
            self.booked_seats_by_show[current_show_key].append(seat_num)

        booked_seats_str = ', '.join(booked_seat_details)
        confirmation_message = (
            f"Booking Confirmed!\n\nMovie: {self.selected_movie}\nShowtime: {self.selected_showtime}\n"
            f"Seats: {booked_seats_str}\nTotal Price: ₹{total_price}"
        )

        messagebox.showinfo("Booking Confirmation", confirmation_message)

        # Reset UI after booking
        self.reset_ui()

    def reset_ui(self):
        self.seat_frame.pack_forget()
        self.book_button.pack_forget()
        self.create_movie_selection_screen()


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieTicketBookingApp(root)
    root.mainloop()
