import tkinter as tk  # Import Tkinter for GUI
from tkinter import messagebox  # Import messagebox for showing alerts/popups
import random  # Import random module for random number generation

# ------------------------------------------------------------
#                  MATHS QUIZ APPLICATION
#        Developed using Python Tkinter GUI Framework
# ------------------------------------------------------------

# ---------------------- MAIN FUNCTIONS ----------------------

def displayMenu():
    """
    Display the main difficulty selection menu.
    Users choose between Easy, Moderate, or Advanced levels.
    """
    clear_window()  # Clear previous widgets from the window

    # Header label
    tk.Label(root, text="🎯 MATHS QUIZ", font=("Arial", 18, "bold"), fg="#0055aa").pack(pady=10)
    tk.Label(root, text="Select Difficulty Level", font=("Arial", 14)).pack(pady=5)

    # Difficulty buttons for three levels
    tk.Button(root, text="1️⃣ Easy", width=20, font=("Arial", 12),
              bg="#d0f0c0", command=lambda: start_quiz('easy')).pack(pady=5)
    tk.Button(root, text="2️⃣ Moderate", width=20, font=("Arial", 12),
              bg="#fff7a5", command=lambda: start_quiz('moderate')).pack(pady=5)
    tk.Button(root, text="3️⃣ Advanced", width=20, font=("Arial", 12),
              bg="#ffb3b3", command=lambda: start_quiz('advanced')).pack(pady=5)


def randomInt(level):
    """
    Generate random integers based on difficulty level.
    - Easy: single-digit numbers (1–9)
    - Moderate: two-digit numbers (10–99)
    - Advanced: four-digit numbers (1000–9999)
    """
    if level == 'easy':
        return random.randint(1, 9)
    elif level == 'moderate':
        return random.randint(10, 99)
    elif level == 'advanced':
        return random.randint(1000, 9999)


def decideOperation():
    """Randomly choose between addition and subtraction."""
    return random.choice(['+', '-'])


def displayProblem():
    """
    Display the current arithmetic problem and input field.
    Also updates the question progress indicator.
    """
    global num1, num2, op, answer_entry, question_label, answer_attempts

    clear_window()  # Remove all existing widgets before showing new question

    # Generate new random numbers and operator based on difficulty
    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    op = decideOperation()

    # Display question number and total
    tk.Label(root, text=f"Question {current_question}/10", font=("Arial", 14, "bold"), fg="#333").pack(pady=5)

    # Display the arithmetic question
    question_label = tk.Label(root, text=f"{num1} {op} {num2} = ?", font=("Arial", 20, "bold"))
    question_label.pack(pady=15)

    # Input box for user's answer
    answer_entry = tk.Entry(root, font=("Arial", 16), justify="center")
    answer_entry.pack(pady=10)
    answer_entry.focus()  # Auto-focus input field

    # Submit button to check answer
    tk.Button(root, text="Submit", font=("Arial", 12, "bold"), bg="#99ccff",
              command=checkAnswer).pack(pady=10)

    # Show current score below the question
    tk.Label(root, text=f"Current Score: {score}", font=("Arial", 12, "italic"), fg="#666").pack(pady=5)


def isCorrect(user_answer, correct_answer):
    """Return True if the user's answer matches the correct one."""
    return user_answer == correct_answer


def checkAnswer():
    """
    Evaluate the user's response.
    - If correct on first attempt → +10 points
    - If correct on second attempt → +5 points
    - Otherwise → 0 points
    """
    global score, current_question, answer_attempts

    try:
        # Convert user input to integer
        user_answer = int(answer_entry.get())
    except ValueError:
        # Handle non-numeric input
        messagebox.showwarning("Invalid Input", "Please enter a valid number.")
        return

    # Calculate the correct answer dynamically
    correct_answer = eval(f"{num1}{op}{num2}")

    # Compare user's answer
    if isCorrect(user_answer, correct_answer):
        # Award full points if first attempt
        if answer_attempts == 0:
            score += 10
            messagebox.showinfo("Correct!", "Excellent! +10 points.")
        else:
            # Award half points if second attempt
            score += 5
            messagebox.showinfo("Correct!", "Good! +5 points.")
        next_question()
    else:
        # If incorrect first time, allow one more try
        if answer_attempts == 0:
            answer_attempts += 1
            messagebox.showwarning("Incorrect", "Try again!")
        else:
            # After two wrong tries, move on to next question
            messagebox.showinfo("Wrong", f"Wrong again! The correct answer was {correct_answer}.")
            next_question()


def next_question():
    """Proceed to the next question or display the final results."""
    global current_question, answer_attempts
    current_question += 1  # Move to next question
    answer_attempts = 0  # Reset attempt counter

    # Continue if fewer than 10 questions
    if current_question <= 10:
        displayProblem()
    else:
        displayResults()  # End quiz and show final results


def displayResults():
    """
    Show final score summary with grade ranking and options
    to replay or exit the quiz.
    """
    clear_window()  # Clear screen before displaying results

    # Show quiz completion message and total score
    tk.Label(root, text="🏁 QUIZ COMPLETE!", font=("Arial", 18, "bold"), fg="#004488").pack(pady=10)
    tk.Label(root, text=f"Your Final Score: {score}/100", font=("Arial", 16)).pack(pady=10)

    # Assign grade and color based on score
    if score >= 90:
        rank = "A+ (Excellent!)"
        color = "#00b300"
    elif score >= 80:
        rank = "A (Great Job!)"
        color = "#33cc33"
    elif score >= 70:
        rank = "B (Good Effort)"
        color = "#66cc66"
    elif score >= 60:
        rank = "C (Needs Practice)"
        color = "#ff9933"
    else:
        rank = "Needs Improvement"
        color = "#ff3333"

    # Display rank with color-coded message
    tk.Label(root, text=f"Your Rank: {rank}", font=("Arial", 14, "italic"), fg=color).pack(pady=10)

    # Buttons to replay or exit the quiz
    tk.Button(root, text="Play Again", width=15, font=("Arial", 12), bg="#99e699",
              command=displayMenu).pack(pady=5)
    tk.Button(root, text="Exit", width=15, font=("Arial", 12), bg="#ff8080",
              command=root.quit).pack(pady=5)


def start_quiz(level):
    """
    Initialize quiz state and start the first question.
    Resets score and counters for a fresh play.
    """
    global difficulty, score, current_question, answer_attempts
    difficulty = level  # Store chosen difficulty
    score = 0  # Reset score
    current_question = 1  # Start from first question
    answer_attempts = 0  # Reset attempt counter
    displayProblem()  # Show first question


def clear_window():
    """Utility function to clear all widgets from the window."""
    for widget in root.winfo_children():
        widget.destroy()  # Remove all elements from main window


# ---------------------- MAIN GUI SETUP ----------------------

# Initialize main Tkinter window
root = tk.Tk()
root.title("🧮 Maths Quiz Challenge")  # Set window title
root.geometry("420x400")  # Set fixed window size
root.resizable(False, False)  # Disable resizing
root.config(bg="#f8f8f8")  # Set background color

# Start the quiz menu when program launches
displayMenu()

# Run Tkinter’s event loop
root.mainloop()