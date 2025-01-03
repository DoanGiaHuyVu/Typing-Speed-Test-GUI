import tkinter as tk
import requests
import random

# Fetch the word list from the website
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(word_site)
WORDS = response.content.splitlines()

# Decode the words from bytes to strings and filter words with 5 characters
WORDS = [word.decode("utf-8") for word in WORDS]
WORDS = [word for word in WORDS if len(word) == 5]

# Two lists to store displayed words and user input words
displayed_words = []
user_words = []
time_left = 60  # Timer starts with 60 seconds
countdown_left = 3  # Countdown starts with 3 seconds
timer_running = False  # To track if the timer is running

# Initialize the count of words typed by the user
word_count = 0


# Function to handle space key press event (random word display and add user input)
def on_space(event=None):
    global word_count
    if user_input['state'] == tk.NORMAL:  # Only proceed if the input is enabled
        # Display a random 5-character word
        random_word = random.choice(WORDS)
        word_label.config(text=random_word)  # Update the label with the random word
        displayed_words.append(random_word)  # Add word to the displayed_words list

        # Add user input word to the user_words list
        user_word = user_input.get().strip()
        if user_word:  # Only add if user has typed something
            user_words.append(user_word)
            word_count += 1  # Increment word count
        user_input.delete(0, tk.END)  # Clear the input field after adding


# Function to update the timer display for the main timer
def update_timer():
    global time_left, word_count
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time left: {time_left} seconds")
        root.after(1000, update_timer)  # Call this function again in 1 second
    else:
        # Time is up, disable the input field and show word count
        user_words.append(user_input.get().strip())
        word_count += 1
        user_input.config(state=tk.DISABLED)
        timer_label.config(text="Time's up! Input disabled.")
        word_count_label.config(text=f"Words Typed: {word_count}")  # Show the word count
        evaluate_performance()  # Call to evaluate performance when time is up


# Function to update the countdown display
def countdown():
    global countdown_left
    if countdown_left > 0:
        timer_label.config(text=f"Starting in: {countdown_left} seconds")
        countdown_left -= 1
        root.after(1000, countdown)  # Call this function again in 1 second
    else:
        timer_label.config(text="Go!")  # Indicate the start
        root.after(1000, start_timer)  # Start the main timer after 1 second


# Function to start the timer
def start_timer():
    global timer_running
    if not timer_running:  # Only start if the timer is not already running
        timer_running = True
        user_input.config(state=tk.NORMAL)  # Enable the input field
        user_input.delete(0, tk.END)
        timer_label.config(text=f"Time left: {time_left} seconds")  # Reset the timer label
        on_space()  # Display a random word immediately when the timer starts
        update_timer()  # Start the timer countdown


# Function to handle the start button click
def initiate_timer():
    global countdown_left, timer_running, word_count, displayed_words, user_words
    countdown_left = 3  # Reset the countdown to 3 seconds
    timer_running = False  # Reset the timer running flag
    user_input.config(state=tk.DISABLED)  # Disable user input
    word_count = 0  # Reset word count
    word_count_label.config(text="")  # Hide the word count display
    result_label.config(text="")  # Reset the result label display
    displayed_words.clear()  # Clear previous displayed words
    user_words.clear()  # Clear previous user input words
    user_input.delete(0, tk.END)  # Clear the input field
    countdown()  # Start the countdown


# Function to reset the game
def reset_game():
    global displayed_words, user_words, time_left, countdown_left, timer_running, word_count
    displayed_words.clear()  # Clear displayed words
    user_words.clear()  # Clear user input words
    time_left = 60  # Reset timer
    countdown_left = 3  # Reset countdown
    timer_running = False  # Reset timer running flag
    word_count = 0  # Reset word count

    word_count_label.config(text="")  # Hide the word count display
    result_label.config(text="")  # Reset result label display
    user_input.delete(0, tk.END)  # Clear the input field
    user_input.config(state=tk.DISABLED)  # Disable input until start
    timer_label.config(text=f"Time left: {time_left} seconds")  # Reset timer label
    word_label.config(text="Press Start to begin!")  # Reset word label


# Function to evaluate performance after the timer ends
def evaluate_performance():
    correct_count = 0
    wrong_count = 0
    total_time = 60  # Total time allowed for typing
    if word_count > 0:
        # Compare displayed words with user input
        for i in range(min(len(displayed_words), len(user_words))):
            if displayed_words[i] == user_words[i]:
                correct_count += 1
            else:
                wrong_count += 1

        # Calculate words per minute (WPM)
        wpm = (word_count / total_time) * 60
        result_label.config(text=f"Correct: {correct_count}, Wrong: {wrong_count}, WPM: {int(wpm)}")
    else:
        result_label.config(text="No words typed.")


# Set up the GUI
root = tk.Tk()
root.title("Random 5-Character Word & User Input Tracker with Timer")

# Add a label to display the random word
word_label = tk.Label(root, text="Press Space for a Random 5-Character Word", font=("Helvetica", 18))
word_label.pack(pady=10)

# Entry widget for user input
user_input = tk.Entry(root, font=("Helvetica", 14), state=tk.DISABLED)  # Initially disabled
user_input.pack(pady=10)

# Timer label to show time left
timer_label = tk.Label(root, text=f"Time left: {time_left} seconds", font=("Helvetica", 14))
timer_label.pack(pady=10)

# Label to show the count of words typed (initially hidden)
word_count_label = tk.Label(root, text="", font=("Helvetica", 14))  # Start with an empty label
word_count_label.pack(pady=10)

# Label to show evaluation results
result_label = tk.Label(root, text="", font=("Helvetica", 14))  # Start with an empty label
result_label.pack(pady=10)

# Button to start the timer
start_button = tk.Button(root, text="Start Timer", command=initiate_timer, font=("Helvetica", 14))
start_button.pack(pady=10)

# Button to reset the game
reset_button = tk.Button(root, text="Reset", command=reset_game, font=("Helvetica", 14))
reset_button.pack(pady=10)

# Display initial instructions
instruction_label = tk.Label(root, text="Type a word and press Space to add it and show a random word",
                             font=("Helvetica", 14))
instruction_label.pack(pady=10)

# Bind the Space key to the on_space function
root.bind('<space>', on_space)

# Start the GUI event loop
root.mainloop()

# For testing purposes, print both lists after closing the window:
print("Displayed Words:", displayed_words)
print("User Input Words:", user_words)
