# %%
from tkinter import *
from PIL import ImageTk, Image
import random
import pygame  # For playing sound

class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.exit_fullscreen)

        pygame.mixer.init()  # Initialize the pygame mixer for sound

        # Initialize variables
        self.player_name = ""
        self.player_score = 0
        self.computer_score = 0
        self.draws = 0
        self.total_rounds = 5
        self.current_round = 0

        # Load and resize background image
        self.bg_image = Image.open('istockphoto-1227598160-612x612.png')  # Replace with your image path
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas and set the background image
        self.canvas = Canvas(root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        self.background = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Title label
        self.title_label = Label(root, text="Rock Paper Scissors - Best of 5 Rounds", font=("Helvetica", 24), bg="white")
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Entry to capture player's name
        self.name_label = Label(root, text="Enter your name to start:", font=("Helvetica", 18), bg="white")
        self.name_label.place(relx=0.5, rely=0.2, anchor="center")

        self.name_entry = Entry(root, font=("Helvetica", 18))
        self.name_entry.place(relx=0.5, rely=0.3, anchor="center")

        self.start_button = Button(root, text="Start Game", font=("Helvetica", 18), bg="lightblue", command=self.start_game)
        self.start_button.place(relx=0.5, rely=0.4, anchor="center")

        # Result, round, and score labels (hidden initially)
        self.round_label = Label(root, text="Round: 1/5", font=("Helvetica", 18), bg="white")
        self.score_label = Label(root, text="", font=("Helvetica", 18), bg="white")
        self.result_label = Label(root, text="", font=("Helvetica", 18), bg="white")

        # Game buttons as text buttons (hidden initially)
        self.rock_button = Button(root, text="Rock", command=lambda: self.play("Rock"), font=("Helvetica", 18), bg="lightblue")
        self.paper_button = Button(root, text="Paper", command=lambda: self.play("Paper"), font=("Helvetica", 18), bg="lightgreen")
        self.scissors_button = Button(root, text="Scissors", command=lambda: self.play("Scissors"), font=("Helvetica", 18), bg="lightcoral")

        # Restart and Close buttons (hidden initially)
        self.restart_button = Button(root, text="Restart", command=self.reset_game, font=("Helvetica", 18), bg="yellow")
        self.close_button = Button(root, text="Close", command=self.close_game, font=("Helvetica", 18), bg="red")

    def start_game(self):
        """Start the game after the player enters their name."""
        self.player_name = self.name_entry.get() or "Player"
        self.name_label.place_forget()
        self.name_entry.place_forget()
        self.start_button.place_forget()

        # Show game elements
        self.round_label.place(relx=0.5, rely=0.1, anchor="center")
        self.score_label.place(relx=0.5, rely=0.15, anchor="center")
        self.result_label.place(relx=0.5, rely=0.4, anchor="center")

        self.rock_button.place(relx=0.3, rely=0.6, anchor="center")
        self.paper_button.place(relx=0.5, rely=0.6, anchor="center")
        self.scissors_button.place(relx=0.7, rely=0.6, anchor="center")

        self.restart_button.place(relx=0.5, rely=0.8, anchor="center")
        self.close_button.place(relx=0.5, rely=0.9, anchor="center")

        # Initialize round and score labels
        self.update_labels()

    def update_labels(self):
        """Update round and score labels."""
        self.round_label.config(text=f"Round: {self.current_round + 1}/{self.total_rounds}")
        self.score_label.config(text=f"{self.player_name}: {self.player_score} | Computer: {self.computer_score} | Draws: {self.draws}")

    def play(self, user_choice):
        if self.current_round >= self.total_rounds:
            return  # Game over, don't play further rounds

        self.current_round += 1
        computer_choice = random.choice(["Rock", "Paper", "Scissors"])
        result = self.determine_winner(user_choice, computer_choice)
        self.result_label.config(text=f"You chose: {user_choice}\nComputer chose: {computer_choice}\n{result}")
        self.update_labels()

        # Play sound effects
        if result == "You win!":
            pygame.mixer.Sound("goodresult-82807.mp3").play()  # Replace with your win sound file
        elif result == "You lose!":
            pygame.mixer.Sound("you-lose-game-sound-230514.mp3").play()  # Replace with your lose sound file
        elif result == "It's a draw!":
            pygame.mixer.Sound("game-fail-90322.mp3").play()  # Replace with your draw sound file

        # If all rounds are over, display the final result
        if self.current_round == self.total_rounds:
            self.end_game()

    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            self.draws += 1
            return "It's a draw!"
        elif (user_choice == "Rock" and computer_choice == "Scissors") or \
             (user_choice == "Paper" and computer_choice == "Rock") or \
             (user_choice == "Scissors" and computer_choice == "Paper"):
            self.player_score += 1
            return "You win!"
        else:
            self.computer_score += 1
            return "You lose!"

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.draws = 0
        self.current_round = 0
        self.result_label.config(text="")
        self.update_labels()

        # Enable game buttons
        self.rock_button.config(state="normal")
        self.paper_button.config(state="normal")
        self.scissors_button.config(state="normal")

    def close_game(self):
        self.root.destroy()  # Properly close the application

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def end_game(self):
        # Automatically display the final results when all rounds are finished
        if self.player_score > self.computer_score:
            final_message = f"Congratulations, {self.player_name}! You won the game!"
        elif self.computer_score > self.player_score:
            final_message = f"Sorry, {self.player_name}. You lost the game."
        else:
            final_message = f"It's a tie! Well played, {self.player_name}!"
        
        # Display the final score and message
        self.result_label.config(text=f"{final_message}\nFinal Scores - {self.player_name}: {self.player_score}, Computer: {self.computer_score}, Draws: {self.draws}")

        # Disable further button presses after game ends
        self.rock_button.config(state="disabled")
        self.paper_button.config(state="disabled")
        self.scissors_button.config(state="disabled")

        # Optionally, show restart button after game ends
        self.restart_button.config(state="normal")


if __name__ == "__main__":
    root = Tk()
    app = RockPaperScissors(root)
    root.mainloop()

# %%



