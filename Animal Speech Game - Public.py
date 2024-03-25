import tkinter as tk
from tkinter import Label, Text, Button, messagebox, font
from PIL import Image, ImageTk
import speech_recognition as sr
import random

# Update the file path to match your system
filepath = r"doc\\"

animals = [
    ["cat.jpg", "cat", "meow"],
    ["dog.jpg", "dog", "woof"],
    ["pig.jpg", "pig", "oink"],
    ["horse.jpg", "horse", "neigh"]
]

class AnimalGuessingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Guess the Animal")

        # set font style
        self.customFont = font.Font(family="Helvetica", size=12)
        self.buttonFont = font.Font(family="Arial", size=10, weight="bold")

        # Set the background color
        self.master.configure(bg='#f0f0f0')

        self.score = 0

        # fonts
        self.score_label = Label(master, text=f"Score: {self.score}", font=self.customFont, bg='#f0f0f0')
        self.score_label.pack(anchor='ne')

        self.label = None  # where animal image goes

        # Initialize the text widget here
        self.text = Text(master, height=4, width=50, font=self.customFont)
        self.text.pack()
        self.text.insert(tk.END, "Click 'Start Listening' to begin.")

        # button styles
        self.start_button = Button(master, text="Start Listening", command=self.detect_voice, font=self.buttonFont, bg='#add8e6')
        self.start_button.pack()

        self.next_button = Button(master, text="Next Animal", state='disabled', command=self.setup_game, font=self.buttonFont, bg='#90ee90')
        self.next_button.pack()

        self.quit_button = Button(master, text="Quit", command=master.quit, font=self.buttonFont, bg='#ffcccb')
        self.quit_button.pack()

        self.setup_game()

    def setup_game(self):
        self.animal = random.choice(animals)
        img_path = filepath + self.animal[0]

        try:
            img = Image.open(img_path)
            img = img.resize((400, 400), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            if self.label:
                self.label.config(image=img_tk)
            else:
                self.label = Label(self.master, image=img_tk, bg='#f0f0f0')
                self.label.pack(before=self.text)
            self.label.image = img_tk  # Keep a reference

            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, "Press 'Start Listening' and say the name of the animal or the sound it makes.")
            self.start_button.config(state='normal')
            self.next_button.config(state='disabled')  # Disable until voice detection is attempted
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {e}")

    def detect_voice(self):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, "Listening... Please speak now.\n")

        r = sr.Recognizer()
        with sr.Microphone() as source:
            #r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio).lower()
                self.text.insert(tk.END, f"Recognised: {text}\n")
                points = self.check_answer(text)
                if points > 0:
                    # Correct answer, update score and provide feedback
                    self.score += points
                    self.score_label.config(text=f"Score: {self.score}")
                    self.text.insert(tk.END, f"You earned {points} points. The correct answers are '{self.animal[1]}' or '{self.animal[2]}'.\n")
                    self.next_button.config(state='normal')  # Enable "Next Animal" button
                    self.start_button.config(state='disabled')  # Disable "Start Listening" button
                else:
                    # Incorrect answer, allow another try
                    self.text.insert(tk.END, "That's not quite right. Try again!\n")
                    self.start_button.config(state='normal')  # Re-enable "Start Listening" button for another attempt
            except sr.UnknownValueError:
                self.text.insert(tk.END, "Could not understand audio. Please try again.\n")
                # Re-enable "Start Listening" for another attempt
                self.start_button.config(state='normal')
            except sr.RequestError as e:
                self.text.insert(tk.END, f"Could not request results; {e}\n")
                # Consider re-enabling "Start Listening" if requests fail
                self.start_button.config(state='normal')

    def check_answer(self, user_answer):
        if user_answer == self.animal[1]:
            return 2
        elif user_answer in self.animal[2]:
            return 1
        else:
            return 0

def main():
    root = tk.Tk()
    app = AnimalGuessingGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

