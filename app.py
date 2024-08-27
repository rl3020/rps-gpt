from flask import Flask, render_template, request, redirect, url_for, jsonify
from rps import Game
import pprint
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
game = Game()
print(__name__)


@app.route("/", methods=['GET'])
def index():
    game_status = game.get_current_game_status()
    return render_template('index.html', game_status=game_status)


@app.route("/submit_choice", methods=['POST'])
def handle_post():
    """
    Returns render_template with appropriate errors.
    """
    # Get user submission data
    user_choice = request.form.get("choice")
    errors = ''

    # Check if submission is complete.
    if user_choice is None:
        errors = 'You did not enter your choice!'
        game_status = game.get_current_game_status()
        return render_template('index.html', errors=errors, game_status=game_status)
    else:
        game_status = game.play_round(user_choice=user_choice)
        return render_template('index.html', errors=errors, game_status=game_status)


@app.route('/chat', methods=["POST"])
def chat():
    user_comment = request.get_json().get("user_comment")
    print("USER COMMENTED:")
    print(user_comment)
    gpt_response = game.chat(user_comment)
    return jsonify(gpt_response)


@app.route('/new_game')
def new_game():
    game.start_new_game()
    return redirect(url_for('index'))


def print_game_status():
    print("\nCurrent game status: \n")
    game_status = game.get_current_game_status()
    pprint.pp(game_status, compact=True)
