import tkinter as tk
from tkinter import messagebox
from random import randint

class CasinoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Casino Game")
        self.root.geometry("500x250+710+415")
        self.root.configure(bg="#222")

        self.balance = 1000.00
        self.last_number = 0

        # Balance Display
        self.balance_label = tk.Label(root, text=f"Balance: ${self.balance:.2f}", font=("Arial", 14, "bold"), fg="white", bg="#222")
        self.balance_label.pack(pady=10)

        # Last Number Display
        self.last_label = tk.Label(root, text="Last Number: 0", font=("Arial", 12), fg="white", bg="#222")
        self.last_label.pack()

        # Bet Amount Entry + Max Button Frame
        bet_frame = tk.Frame(root, bg="#222")
        bet_frame.pack(pady=5)

        self.bet_label = tk.Label(bet_frame, text="Enter your bet:", font=("Arial", 12), fg="white", bg="#222")
        self.bet_label.pack(side="left", padx=5)

        self.bet_entry = tk.Entry(bet_frame, font=("Arial", 12), width=10)
        self.bet_entry.pack(side="left")

        self.max_button = tk.Button(bet_frame, text="Max", font=("Arial", 10), bg="gray", fg="white", command=self.set_max_bet)
        self.max_button.pack(side="left", padx=5)

        # Betting Buttons Frame
        self.button_frame = tk.Frame(root, bg="#222")
        self.button_frame.pack(pady=10)

        # Game Buttons (Pair/Odd or Higher/Lower/Equal)
        self.option_buttons = []
        self.setup_pair_odd_buttons()

        # Quit Button
        self.quit_button = tk.Button(root, text="Quit", font=("Arial", 12, "bold"), bg="red", fg="white", command=root.quit)
        self.quit_button.pack(pady=10)

    def set_max_bet(self):
        """Set the bet entry to the player's full balance."""
        self.bet_entry.delete(0, tk.END)
        self.bet_entry.insert(0, f"{self.balance:.2f}")

    def setup_pair_odd_buttons(self):
        """Sets up the Pair/Odd betting buttons when last number is 0 or 100."""
        self.clear_buttons()
        pair_btn = tk.Button(self.button_frame, text="Pair (x2)", font=("Arial", 12), bg="blue", fg="white",
                             command=lambda: self.play_game("p"))
        odd_btn = tk.Button(self.button_frame, text="Odd (x2)", font=("Arial", 12), bg="purple", fg="white",
                            command=lambda: self.play_game("o"))
        pair_btn.grid(row=0, column=0, padx=10, pady=5)
        odd_btn.grid(row=0, column=1, padx=10, pady=5)
        self.option_buttons.extend([pair_btn, odd_btn])

    def setup_higher_lower_buttons(self):
        """Sets up the Higher/Lower/Equal betting buttons for all other cases."""
        self.clear_buttons()
        payout_low = round(1 / (self.last_number / 100), 2)
        payout_high = round(1 / ((100 - self.last_number) / 100), 2)

        low_btn = tk.Button(self.button_frame, text=f"Lower (x{payout_low})", font=("Arial", 12), bg="orange", fg="white",
                            command=lambda: self.play_game("l"))
        equal_btn = tk.Button(self.button_frame, text="Equal (x100)", font=("Arial", 12), bg="gold", fg="black",
                              command=lambda: self.play_game("e"))
        high_btn = tk.Button(self.button_frame, text=f"Higher (x{payout_high})", font=("Arial", 12), bg="green", fg="white",
                             command=lambda: self.play_game("h"))

        low_btn.grid(row=0, column=0, padx=10, pady=5)
        equal_btn.grid(row=0, column=1, padx=10, pady=5)
        high_btn.grid(row=0, column=2, padx=10, pady=5)

        self.option_buttons.extend([low_btn, equal_btn, high_btn])

    def clear_buttons(self):
        """Clears the betting buttons."""
        for btn in self.option_buttons:
            btn.destroy()
        self.option_buttons = []

    def play_game(self, guess):
        """Handles the game logic and updates the UI."""
        try:
            bet = float(self.bet_entry.get())
            if bet < 0.01 or bet > self.balance:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Bet", "Enter a valid bet amount!")
            return

        self.balance -= bet
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

        # Generate the new random number
        new_number = randint(0, 100)

        # Determine result
        if self.last_number == 0 or self.last_number == 100:
            # Pair/Odd Case
            result_text = f"The new number is {new_number}! "
            if new_number == 0:
                result_text += "O is not considered pair or impair in this game."
            elif new_number % 2 == 0:
                result_text += "It's a pair number."
                if guess == "p":
                    winnings = bet * 2
                    self.balance += winnings
                    result_text += f" You win ${winnings:.2f}!"
            else:
                result_text += "It's an odd number."
                if guess == "o":
                    winnings = bet * 2
                    self.balance += winnings
                    result_text += f" You win ${winnings:.2f}!"
        else:
            # Higher/Lower/Equal Case
            payout_low = round(1 / (self.last_number / 100), 2)
            payout_high = round(1 / ((100 - self.last_number) / 100), 2)

            result_text = f"The new number is {new_number}! "
            if new_number == self.last_number:
                result_text += "It's the same!"
                if guess == "e":
                    winnings = bet * 100
                    self.balance += winnings
                    result_text += f" You win ${winnings:.2f}!"
            elif new_number < self.last_number:
                result_text += "It's lower."
                if guess == "l":
                    winnings = round(bet * payout_low, 2)
                    self.balance += winnings
                    result_text += f" You win ${winnings:.2f}!"
            else:
                result_text += "It's higher."
                if guess == "h":
                    winnings = round(bet * payout_high, 2)
                    self.balance += winnings
                    result_text += f" You win ${winnings:.2f}!"

        # Update last number
        self.last_number = new_number
        self.last_label.config(text=f"Last Number: {self.last_number}")

        # Show result popup
        messagebox.showinfo("Result", result_text)

        # Update balance display
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

        # Switch game mode if needed
        if self.last_number == 0 or self.last_number == 100:
            self.setup_pair_odd_buttons()
        else:
            self.setup_higher_lower_buttons()

        # Check if player is bankrupt
        if self.balance < 0.01:
            messagebox.showwarning("Game Over", "You're out of money! Game Over.")
            self.root.quit()


# Run the Game
root = tk.Tk()
game = CasinoGame(root)
root.mainloop()
