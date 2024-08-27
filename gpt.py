from openai import OpenAI
from dotenv import load_dotenv
import json


class Gpt:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()
        program = "You are playing a game of rock, paper, scissors against a user. " +\
            "The user will either 1. talk trash to you or 2. submit their choice of rock, paper or scissors." +\
            "If a user says trash talk to you, then you should respond with trash talk." +\
            "Otherwise, when the user makes a guess, which I will tell you when the user made their guess, " +\
            "you should respond with your own choice. To do this respond with JSON with a field named 'choice', with your" +\
            "choice of either 'rock', 'paper', or 'scissors'."

        self.messages = [
            {"role": "system", "content": program},
        ]

    def get_gpt_choice(self):
        """
        returns gpt trash_talk
        {'choice': 'rock'}
        """
        prompt = "The user has made their choice, so make your choice now. "
        prompt += "Respond with a json object with a field of 'choice', with your choice of either 'rock','paper', or 'scissors'."

        self.messages.append({"role": "user", "content": prompt})

        completion = self.client.chat.completions.create(
            response_format={"type": "json_object"},
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        gpt_data = json.loads(completion.choices[0].message.content)
        print(gpt_data)
        return gpt_data

    def get_gpt_trash_talk(self, trash_talk):
        """
        returns gpt trash_talk
        {'trash_talk': 'you suck!!'}
        """
        prompt = "The user said this to you: "
        prompt += "'" + trash_talk + "'. "
        prompt += "Respond to this user and remember to be sassy."
        prompt += "Remeber to use json object with a field of 'trash_talk'."

        self.messages.append({"role": "user", "content": prompt})

        completion = self.client.chat.completions.create(
            response_format={"type": "json_object"},
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        gpt_data = json.loads(completion.choices[0].message.content)
        print("GPT CHAT RESPONSE: ", gpt_data)
        return gpt_data

    def get_gpt_round_reaction(self, outcome):
        """
        returns gpt trash_talk
        {'trash_talk': 'you suck!!'}
        """
        prompt = "The outcome of the game is that you: " + outcome + "."
        prompt += "Respond to this outcome with JSON with a field of 'trash_talk'."

        self.messages.append({"role": "user", "content": prompt})

        completion = self.client.chat.completions.create(
            response_format={"type": "json_object"},
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        gpt_data = json.loads(completion.choices[0].message.content)
        print(gpt_data)
        return gpt_data
