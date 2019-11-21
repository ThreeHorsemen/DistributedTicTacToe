from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import socket

from random import randrange
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

state = {}
state['number_of_players'] = 0
game = []

id = 0
winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

@app.route('/game', methods = ['GET'])
@cross_origin()
def foo():
    global id
    global state
    global game
    state['winner'] = 0
    state['turn'] = 0

    if state['number_of_players'] < 2:
        id += 1
        state['number_of_players'] += 1

        if  state['number_of_players'] == 1:
            state['player1'] = id
        else:
            state['player2'] = id

            x = randrange(1, 100)
            game = [0 for i in range(9)]

            if x <= 50:
                state['turn'] = state['player1']
            else:
                state['turn'] = state['player2']

        return jsonify(id = id, status = True)
    else:
        return jsonify(status= False)


@app.route('/heartbeat', methods = ['POST'])
@cross_origin()
def heartbeat():
    global state
    global game
    data = request.json
    rid = data['id']

    if state['winner'] != 0:

        ret = jsonify(value= True, game_ongoing= False, winner = state['winner'], game=game )

        if rid not in state['players_informed_of_winner']:
            state['players_informed_of_winner'].append(rid)

        if len(state['players_informed_of_winner']) == 2:
            reset_game()
            
        return ret

    if state['turn'] == rid:
        return jsonify(value= True, game=game, game_ongoing= True)
    else:
        return jsonify(value=False, game=game, game_ongoing= True)


@app.route('/turn', methods = ['POST'])
@cross_origin()
def process_turn():
    global state
    global game
    data = request.json
    move = data['index']
    rid = data['id']

    if game[move] != 0:
        return jsonify(value=False, game=game)
    else:
        game[move] = rid 

        if check_if_game_has_been_won():
            state['winner'] = rid
            state['players_informed_of_winner'] = []

        
        if state['turn'] == state['player1']:
            state['turn'] = state['player2']
        else:
            state['turn'] = state['player1']
        
        return jsonify(value=True, game=game)



@app.route('/')
@cross_origin()
def main_page():
    return jsonify(value='TicTacToe')

def reset_game():
    global state
    global game
    state = {}
    state['number_of_players'] = 0
    game = []


def check_if_game_has_been_won():
    global winning_combinations
    global game

    for c in winning_combinations:
        if (game[c[0]] == game[c[1]] == game[c[2]]) and (game[c[0]] != 0):
            return True
    return False


if __name__ == '__main__':

    app.run()