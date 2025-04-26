import requests
import telebot
import sys

Token = '6968241390:AAHrtDMpdsajpBtnVsvnhAAbJWlyLjEAl08'
bot = telebot.TeleBot(Token)

class User:
    def __init__(self, message) -> None:
        self.fname = message.from_user.first_name
        self.lname = message.from_user.last_name
        self.uname = message.from_user.username
        self.usrid = message.from_user.id

class Brian:
    def __init__(self, text):
        self.text = text

    def save_ogg(self):
        temp = requests.get(
            url=f"https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={self.text}",
            stream=True,
            timeout=5,
        )
        with open("out.ogg", "wb") as file:
            for chunk in temp:
                file.write(chunk)

@bot.message_handler(commands=["start"])
def start_command(message):
    user = User(message)
    name = user.fname if user.fname is not None else f"Unknown User"
    Brian(f"Hello {name}! Welcome to the trolling experience. Prepare for some laughs!").save_ogg()
    bot.send_message(message.chat.id, f"Hello {name}! Welcome to the trolling experience. Prepare for some laughs!")
    with open("out.ogg", "rb") as voice:
        bot.send_voice(message.chat.id, voice)
    print(f"Sent voice to User '{name}' ({user.usrid})")

@bot.message_handler(func=lambda _: True)
def echo_all(message):
    user = User(message)
    name = user.fname if user.fname is not None else f"Unknown User"
    Brian(message.text.strip()).save_ogg()
    bot.send_message(message.chat.id, f"Here's your transformed message, {name}!")
    with open("out.ogg", "rb") as voice:
        bot.send_voice(message.chat.id, voice, message.text)
    print(f"Sent voice to User '{name}' ({user.usrid})")

if __name__ == "__main__":
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("Exit requested by user.")
        sys.exit()
