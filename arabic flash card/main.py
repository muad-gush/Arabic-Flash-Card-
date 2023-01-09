from tkinter import *
import pandas
import random
import PIL.Image
import PIL.ImageTk

BACKGROUND_COLOR = "#856ff8"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv(r"Python/arabic flash card/data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv(r"Python/arabic flash card/data/arabic words translated to english.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Arabic", fill="black")
    canvas.itemconfig(card_word, text=current_card["Arabic"], fill="black")
    canvas.itemconfig(card_background, image=front_photo)
    flip_timer = window.after(5000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=back_photo)


def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv(r"Python/arabic flash card/data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
front_card = PIL.Image.open(r"Python/arabic flash card/images/card_front.png")
back_card = PIL.Image.open(r"Python/arabic flash card/images/card_back.png")
front_photo = PIL.ImageTk.PhotoImage(front_card)
back_photo = PIL.ImageTk.PhotoImage(back_card)

card_background = canvas.create_image(400, 263, image=front_photo)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file=r"Python/arabic flash card/images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file=r"Python/arabic flash card/images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()