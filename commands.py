import subprocess
import os
from get_answer import Fetcher


class Commander:
    def __init__(self):
        self.confirm = ["yes", "affirmative", "si", "sure", "do it", "yeah", "confirm"]
        self.cancel = ["no", "negative", "negative soldier", "don't", "wait", "cancel"]

    def discover(self, text):
        """
        Handles various requests submitted as text
        """
        # Handles names
        if "what" in text and "name" in text:
            if "my" in text:
                self.respond("You have not told me your name yet")
            else:
                self.respond("My name is Monty. How are you?")
        # Handles app launch
        elif "launch" in text or "open" in text:
            # 'Launch Mozilla Firefox' becomes 'Mozilla Firefox'
            app = text.split(" ", 1)[-1]
            self.respond("Opening " + app)
            os.system('open -a ' + app + ".app")
        # Handles response lookup
        else:
            fetch = Fetcher("https://www.google.com/search?q=" + text)
            answer = fetch.lookup()
            self.respond(answer)

    def respond(self, response):
        """
        Speech-to-test is handled using 'say' (https://ss64.com/osx/say.html)
        """
        print(response)
        subprocess.call("say '" + response + "'", shell=True)
