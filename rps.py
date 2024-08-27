from gpt import Gpt
import json
import pprint
import html


class Game:
    def __init__(self):
        self.round = 0
        self.user = 0
        self.gpt_points = 0
        self.gpt_choice = ''
        self.user_choice = ''
        self.round_winner = ''
        self.conversation = [{
            'who': 'gpt', 'comment': html.escape('You\'re going to lose this one buddy.')}]

        self.is_complete = False
        self.game_winner = ''
        self.gpt = Gpt()

    def play_round(self, user_choice):
        """
        Returns the the current status of the game in JSON.
        """

        # Get GPTs choice & response to trash talk
        self.user_choice = user_choice
        # Get gpt choice
        gpt_choice = self._get_gpt_choice()
        # See who the winner is.
        self.round_winner = self._get_round_winner(gpt_choice, user_choice)

        # Increment count for the winner
        if self.round_winner == 'user':
            self.user += 1
        elif self.round_winner == 'gpt':
            self.gpt_points += 1

        # Only if it is not a tie, do not increment counter
        if self.round_winner != 'tie':
            self.round += 1

        if self.round == 3:
            self.is_complete = True
            if self.user > self.gpt_points:
                self.game_winner = 'user'
            else:
                self.game_winner = 'gpt'
            return self.get_current_game_status()
        else:
            return self.get_current_game_status()

    def get_current_game_status(self):
        return {
            'round': self.round,
            'round_winner': self.round_winner,
            'gpt_points': self.gpt_points,
            'user': self.user,
            'conversation': self.conversation,
            'is_complete': self.is_complete,
            'gpt_choice': self.gpt_choice,
            'user_choice': self.user_choice,
            'game_winner': self.game_winner
        }

    def start_new_game(self):
        self.round = 0
        self.user = 0
        self.gpt_points = 0
        self.gpt_choice = ''
        self.user_choice = ''
        self.round_winner = ''
        self.conversation = [{
            'who': 'gpt', 'comment': html.escape('You\'re going to lose this one buddy.')}]
        self.is_complete = False
        self.game_winner = ''

    def chat(self, user_comment):
        if not user_comment:
            return

        # escape user comments in case of funky text
        user_comment = html.escape(user_comment)

        # add user comment to conversation
        self._add_to_conversation('user', user_comment)

        # get GPTs response
        gpt_comment = self.gpt.get_gpt_trash_talk(user_comment)

        # add GPT to conversation
        self._add_to_conversation('gpt', gpt_comment.get("trash_talk"))

        # return recent comment
        return gpt_comment

    """
    Utility functions defined below
    """

    def _add_to_conversation(self, who, trash_talk):
        if trash_talk:
            self.conversation.append(
                {'who': who, 'comment': trash_talk})

    def _get_gpt_choice(self):
        """
        Returns:
        {
            'gpt_choice': 'rock',
            'gpt_trash_talk' : 'You suck too, buddy.'
        }
        """
        # call gpt
        use_gpt = False
        response = None
        if use_gpt:
            response = self.gpt.get_gpt_choice()
        else:
            response = {
                'choice': 'rock'
            }

        self.gpt_choice = response.get('choice')
        print("GPT CHOICE: ", self.gpt_choice)
        return self.gpt_choice

    def _get_round_winner(self, gpt_guess, user_guess):
        """
        returns:
        1. tie - if tie
        2. gpt - if gpt wins
        3. user - if user wins
        """
        winner = ''
        if gpt_guess == user_guess:
            return 'tie'

        # Rock case
        if gpt_guess == 'rock':
            if user_guess == 'paper':
                winner = 'user'
            elif user_guess == 'scissors':
                winner = 'gpt'
        # Paper case
        elif gpt_guess == 'paper':
            if user_guess == 'rock':
                winner = 'gpt'
            elif user_guess == 'scissors':
                winner = 'user'
        # Scissors case
        elif gpt_guess == 'scissors':
            if user_guess == 'rock':
                winner = 'user'
            elif user_guess == 'paper':
                winner = 'gpt'

        return winner
