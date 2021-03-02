from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
FONT1 = ("Ariel", 60, "bold")
FONT2 = ("Ariel", 40, "italic")

wordsLeft = {}
currentCard = {}

# read CSV
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    originalData = pandas.read_csv("data/french_words.csv")
    wordsLeft = originalData.to_dict(orient="records")
else:
    wordsLeft = data.to_dict(orient="records")


def nextCard():
    global currentCard, flipTimer
    window.after_cancel(flipTimer)
    currentCard = random.choice(wordsLeft)
    canvas.itemconfig(cardTitle, text="French", fill="black")
    canvas.itemconfig(cardWord, text=currentCard["French"], fill="black")
    canvas.itemconfig(cardBackground, image=flashcardFrontIMG)
    flipTimer = window.after(3000, func=flipCard)


def flipCard():
    canvas.itemconfig(cardTitle, text="English", fill="white")
    canvas.itemconfig(cardWord, text=currentCard["English"], fill="white")
    canvas.itemconfig(cardBackground, image=flashcardBackImage)


def isKnown():
    wordsLeft.remove(currentCard)
    wordsLeftData = pandas.DataFrame(wordsLeft)
    wordsLeftData.to_csv("data/words_to_learn.csv", index=False)
    nextCard()


# UI
window = Tk()
window.title("Flashcard")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flipTimer = window.after(3000, func=flipCard)

canvas = Canvas(height=526, width=800)
flashcardFrontIMG = PhotoImage(file="images/card_front.gif")
flashcardBackImage = PhotoImage(file="images/card_back.gif")
cardBackground = canvas.create_image(400, 263, image=flashcardFrontIMG)
cardTitle = canvas.create_text(400, 263, text="", font=FONT1)
cardWord = canvas.create_text(400, 150, text="", font=FONT2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

checkIMG = PhotoImage(file="images/right.gif")
correctButton = Button(image=checkIMG, highlightthickness=0, command=isKnown)
correctButton.grid(column=0, row=1)

wrongIMG = PhotoImage(file="images/wrong.gif")
wrongButton = Button(image=wrongIMG, highlightthickness=0, command=nextCard)
wrongButton.grid(column=1, row=1)

nextCard()

window.mainloop()
