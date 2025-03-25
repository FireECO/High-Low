# High-Low

## Description
This is a simple casino-style game built with Python's `tkinter` library for the graphical user interface (GUI). The game allows players to place bets and guess whether the next random number will be higher, lower, or equal to the previous one. There are two modes: Pair/Odd (available when the last number is 0 or 100) and Higher/Lower/Equal (available for all other numbers). The player's balance is updated based on their guesses, and they can either win or lose money depending on the outcome. The game continues until the player runs out of money.
A web version of the game is currently being worked on.

## Usage
To run the game, simply execute the Python script. The game interface will appear with the following features:
- **Balance Display:** Shows the current balance of the player.
- **Last Number Display:** Shows the last randomly generated number.
- **Bet Amount Entry:** Allows the player to enter the amount they wish to bet.
- **Max Button:** Automatically sets the bet to the player's full balance.
- **Betting Buttons:** Options to bet on "Pair," "Odd," "Higher," "Lower," or "Equal."
- **Quit Button:** Exits the game.

The player can place bets and make predictions based on the game's current mode. If the player wins, their balance will be updated and displayed. If the player runs out of money, the game will display a "Game Over" message and quit.
