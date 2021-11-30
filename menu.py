import tkinter
from tkinter import *
import tkinter.font as font
import socket
import json
import random, os
from PIL import Image, ImageTk


def how_to_play():
    """Opens when the how to play button is pressed."""
    top = Toplevel(root)
    top.title("How to Play")
    top.configure(background='#0075BE')
    Label(top, bg='#0075BE', fg="#FFCC00", justify=CENTER, text="Simply press play to begin! \n "
                    "Type the name of the Pokémon you think is displayed in the textbox. \n"
                    "You have 3 lives. If you guess wrongly you lose a life. \n"
                    "Press hint if you are stuck to get one letter in the answer! \n"
                    "When you run out of lives it is Game Over and your score will be displayed \n"
                    "Good luck and have fun making new high scores!").pack()

    resize_window(750, 200, top)


def about_pokemon():
    """Opens when the about pokemon button is pressed. Utilizes teammates' wikipedia scraper microservice."""
    top = Toplevel(root)
    top.title("About Pokemon")
    top.configure(background='#0075BE')

    """Begin communication with teammate's microservice."""
    host = socket.gethostname()
    port = 7634

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((host, port))

    """Send query to scrape summary from Pokemon wikipedia page."""
    message = {"url":"https://en.wikipedia.org/wiki/Pokémon", "summary":"true"}
    request = json.dumps(message)

    c.send(request.encode("utf-8"))
    response = c.recv(8196).decode("utf-8")
    parsedResponse = json.loads(response)

    """Place the parsed response in a label."""
    Label(top, bg='#0075BE', fg="#FFCC00", text=parsedResponse["summary"][:971], wraplength=500, justify=CENTER).pack()

    """End socket communication."""
    c.close()

    resize_window(750, 420, top)


def play():
    # Clear the canvas
    canvas.delete('all')
    about_butt.pack_forget()
    how_butt.pack_forget()
    play_butt.pack_forget()
    Label(canvas, bg="#0075BE", font=("Arial", 60, 'bold'), text="Who's that Pokémon?", justify=CENTER).pack()

    path = './pokemon_images/'
    random_poke_image = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))
    ])

    path += random_poke_image
    print(path)

    random_poke = Image.open(path)
    random_poke = random_poke.resize((400, 400), Image.ANTIALIAS)
    random_poke = ImageTk.PhotoImage(random_poke)
    label = Label(image=random_poke, background='#0075BE', justify=CENTER)
    label.image = random_poke
    label.pack()

    # Remove the .png characters
    random_poke_name = random_poke_image[:-4]













def resize_window(w, h, window):
    """Takes as input the width, height and name of new window and centers it."""
    # Set the width and height of the window
    width = w
    height = h

    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    # calculate x and y coordinates for the Tk window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # Set the dimensions of the window and where it is placed
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


root = Tk()

# Set default font to arial
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Arial",
                           size=17,
                           weight=font.BOLD)

# Make a window for the game GUI
root.title("Who's that Pokémon?")

resize_window(900, 750, root)

# set the background color
root.configure(background='#0075BE')

# Buttons
about_butt = tkinter.Button(root, text="About Pokémon", bg="#FFCC00", fg="black", command=about_pokemon, highlightbackground='#FFCC00')
about_butt.config(height=3, width=15)

about_butt.pack(side=BOTTOM, padx='0', pady='10', anchor='center')

how_butt = tkinter.Button(root, text="How to Play", bg="#FFCC00", fg="black", command=how_to_play, highlightbackground='#FFCC00')
how_butt.config(height=3, width=15)

how_butt.pack(side=BOTTOM, padx='0', pady='10', anchor=CENTER)

play_butt = tkinter.Button(root, text="Play", bg="#FFCC00", fg="black", command=play,  highlightbackground='#FFCC00')
play_butt.config(height=3, width=15)

play_butt.pack(side=BOTTOM, padx='0', pady='10', anchor=CENTER)


# Getting both images and resizing
logo = Image.open('./images/logo.png')
logo = logo.resize((400, 400), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
pikachu = Image.open('./images/pikachu.png')
pikachu = pikachu.resize((300, 300), Image.ANTIALIAS)
pikachu = ImageTk.PhotoImage(pikachu)

width, height = logo.width(), logo.height()
canvas = Canvas(root, bg="#0075BE", width=400, height=900, highlightthickness=0)
canvas.pack()
canvas.create_image(10, -100, image=logo, anchor=NW)
canvas.create_image(75, 200, image=pikachu, anchor=NW)

root.mainloop()