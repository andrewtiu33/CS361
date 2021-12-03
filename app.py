import tkinter
from tkinter import *
import tkinter.font as font
import socket
import json
import csv
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

    # Begin communication with teammate's microservice
    host = socket.gethostname()
    port = 7634

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((host, port))

    # Send query to scrape summary from Pokemon wikipedia page
    message = {"url":"https://en.wikipedia.org/wiki/Pokémon", "summary":"true"}
    request = json.dumps(message)

    c.send(request.encode("utf-8"))
    response = c.recv(8196).decode("utf-8")
    parsed_response = json.loads(response)

    # Place the parsed response in a label
    Label(top, bg='#0075BE', fg="#FFCC00", text=parsed_response["summary"][:971], wraplength=500, justify=CENTER).pack()

    # End socket communication
    c.close()
    resize_window(750, 420, top)


def clear_canvas():
    """Clears the canvas."""
    # Clear the canvas and add game title
    canvas.delete('all')
    about_butt.pack_forget()
    how_butt.pack_forget()
    play_butt.pack_forget()


def play():
    """Code that runs when the game is started."""

    def refresh_screen():
        """Refreshes the screen to have a new Pokemon and hint after an answer is entered"""
        new_poke_image, new_poke = get_random_pokemon(poke_list)
        displayed_hint["text"] = ""
        current_poke_label.configure(image=new_poke_image)
        current_poke_label.image = new_poke_image
        nonlocal current_poke_name
        current_poke_name = new_poke[:-4]
        hint["state"] = NORMAL

    def clear_screen():
        """This function removes everything from the screen. Used when game is over"""
        # Remove everything from canvas
        title.pack_forget()
        submit.pack_forget()
        hint.pack_forget()
        your_answer.pack_forget()
        user_input.pack_forget()
        current_poke_label.pack_forget()
        score_label.pack_forget()

    def game_over():
        """Displays game over screen when the game is over."""
        # Display the score
        nonlocal score
        Label(canvas, bg="#0075BE", font=("Arial", 60, 'bold'), text="Congratulations!", justify=CENTER).pack()
        Label(canvas, bg="#0075BE",  font=("Arial", 50, 'bold'), text="Your final score was:", justify=CENTER).pack(pady=30)
        Label(canvas, bg="#0075BE", fg="#FFCC00", font=("Arial", 60, 'bold'), text=str(score), justify=CENTER).pack()

        # Load the end image
        global end_image
        end_image = Image.open('./images/gameover.jpg')
        end_image = ImageTk.PhotoImage(end_image)

        end_image_label = Label(canvas, bg="#0075BE", image=end_image, justify=CENTER)
        end_image_label.pack(pady=30)

    def submit_name(correct_answer):
        """Takes as input the correct answer. Checks if user's input is the correct answer"""
        guess = user_input.get().lower()
        nonlocal question_num
        nonlocal score

        # If the user's guess was correct, add to score, clear hint and switch the image
        if guess == correct_answer:
            score += 10

        # If user's guess was wrong, decrease score, clear hint and switch the image
        else:
            score -= 10

        question_num += 1

        # If the question number is 10, end the game
        if question_num == 11:
            clear_screen()
            game_over()

        # If the question number is not 10, continue the game
        else:
            score_label["text"] = "Current Score: " + str(score)
            refresh_screen()

    def get_hint(pokemon_name):
        """Gives a hint to a user. Calls excel microservice."""
        HOST = 'localhost'  # The server's hostname or IP address
        PORT = 1443  # The port used by the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        message = pokemon_name
        sock.send(message.encode('utf-8'))
        response = sock.recv(400)
        displayed_hint["text"] = response
        print(response)

        # Update score
        nonlocal score
        score -= 5
        score_label["text"] = "Current Score: " + str(score)

        # Disable button
        hint["state"] = DISABLED

    def get_random_pokemon(poke_list):
        path = './pokemon_images/'

        # Choose a random pokemon from the list and then removes it from the pool
        random_poke = random.choice(poke_list)
        poke_list.remove(random_poke)

        path += random_poke
        random_poke_image = Image.open(path)
        random_poke_image = random_poke_image.resize((350, 350), Image.ANTIALIAS)
        random_poke_image = ImageTk.PhotoImage(random_poke_image)
        return random_poke_image, random_poke

    clear_canvas()

    # Track the question number with a counter
    question_num = 1

    # Display the game title
    title = Label(canvas, bg="#0075BE", font=("Arial", 60, 'bold'), text="Who's that Pokémon?", justify=CENTER)
    title.pack()

    # Create a score display label
    score = 0
    score_label = Label(bg="#0075BE", font=("Arial", 30, 'bold'), text="Current Score: " + str(score))
    score_label.pack(pady=10)

    # Get the random pokemon list
    path = './pokemon_images/'
    poke_list = [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))]

    # Remove the ds store file so no errors are caused
    poke_list.remove('.DS_Store')

    # Create a space for the Pokemon image
    current_poke_image, current_poke = get_random_pokemon(poke_list)
    current_poke_label = Label(image=current_poke_image, background='#0075BE', justify=CENTER)
    current_poke_label.image = current_poke_image
    current_poke_label.pack()

    # Remove the .png characters to get the character name to be guessed
    current_poke_name = current_poke[:-4]

    # Create the label for user's answer
    your_answer = Label(bg="#0075BE", font=("Arial", 30, 'bold'), text="Your Answer:")
    your_answer.pack()

    # Create the guess input box
    user_input = Entry(root, font=("Arial", 20), justify="center")
    user_input.pack()
    user_input.focus()

    # Create a submit button
    submit = Button(text="Submit", font=("Arial", 20), width=10, command=lambda: submit_name(current_poke_name))
    submit.pack(pady=20)

    # Create a hint button
    hint = tkinter.Button(root, text="Hint", font=("Arial", 20), width=10, command=lambda: get_hint(current_poke_name))
    hint.pack()

    # Create placeholder for hint
    displayed_hint = Label(bg='#0075BE', fg="#FFCC00", wraplength=500, justify=CENTER)
    displayed_hint.pack(pady=10)


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