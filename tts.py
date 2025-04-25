import requests
import telebot
import os
import sys

#with open("token.env", "r") as config:
 #   Token = config.read().strip().split("=")[1]
Token = '6968241390:AAHrtDMpdsajpBtnVsvnhAAbJWlyLjEAl08'
# Client
bot = telebot.TeleBot(Token)


# User class: which creates a member with needed stuff.
# We need to use user data to do some trolling :D
class User:
    def __init__(self, message) -> None:
        # takes user info from message
        self.fname = message.from_user.first_name
        self.lname = message.from_user.last_name
        self.uname = message.from_user.username
        self.usrid = message.from_user.id


class Brian:
    def __init__(self, text):
        # Takes message and changes it to Brian voice
        self.text = text

    # Saves the voice
    def save_ogg(self):
        temp = requests.get(
            url=f"https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={self.text}",
            stream=True,
            timeout=5,
        )
        with open("out.ogg", "wb") as file:
            for chunk in temp:
                file.write(chunk)


# Start command: will be executed when /start pressed.
@bot.message_handler(commands=["start"])
def start_command(message):
    # Gets user information
    user = User(message)
    name = user.fname if user.fname is not None else f"Unknown User"

    # Gets the voice
    Brian(
        f"Hello {name}! Welcome to the trolling experience. Prepare for some laughs!"
    ).save_ogg()

    # Sends the voice along with a text message
    bot.send_message(message.chat.id, f"Hello {name}! Welcome to the trolling experience. Prepare for some laughs!")
    with open("out.ogg", "rb") as voice:
        bot.send_voice(message.chat.id, voice)
    print(f"Sent voice to User '{name}' ({user.usrid})")


# Echo all messages
@bot.message_handler(func=lambda _: True)
def echo_all(message):
    # Gets user information
    user = User(message)
    name = user.fname if user.fname is not None else f"Unknown User"

    # Gets the voice
    Brian(message.text.strip()).save_ogg()

    # Sends the voice along with a text message
    bot.send_message(message.chat.id, f"Here's your transformed message, {name}!")
    with open("out.ogg", "rb") as voice:
        bot.send_voice(message.chat.id, voice, message.text)
    print(f"Sent voice to User '{name}' ({user.usrid})")


# Runs the bot in infinity mode
if __name__ == "__main__":
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("Exit requested by user.")
        sys.exit()