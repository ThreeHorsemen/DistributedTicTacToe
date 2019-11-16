from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import socket

from random import randrange
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

state = {}
state['number_of_players'] = 0
game = []

id = 0

@app.route('/game', methods = ['GET'])
@cross_origin()
def foo():
    global id

    if state['number_of_players'] < 2:
        id += 1
        state['number_of_players'] += 1

        if  state['number_of_players'] == 1:
            state['player1'] = id
        else:
            state['player2'] = id
            state['winner'] = 0

            x = randrange(1, 100)

            if x <= 50:
                state['turn'] = state['player1']
            else:
                state['turn'] = state['player2']

            game = [0 for i in range(9)]

        return jsonify(id = id, status = True)
    else:
        return jsonify(status= False)


@app.route('/heartbeat', methods = ['POST'])
@cross_origin()
def heartbeat():
    data = json.loads(request.json)
    rid = data['id']

    if state['winner'] != 0:
        state['players_informed_of_winner'] += 1

        if state['players_informed_of_winner'] == 2:
            reset_game()
        return jsonify(value= True, game_ongoing= False, winner = state['winner'], game=game )

    if state['turn'] == rid:
        return jsonify(value= True, game=game, game_ongoing= True)
    else:
        return jsonify(value=False, game_ongoing= True)


@app.route('/turn', methods = ['POST'])
@cross_origin()
def process_turn():
    data = json.loads(request.json)
    move = data['index']
    rid = data['id']

    if game[move] != 0:
        return jsonify(value=False)
    else:
        game[move] = rid 

        if check_if_game_has_been_won():
            state['winner'] = rid
            state['players_informed_of_winner'] = 0

        
        if state['turn'] == state['player1']:
            state['turn'] = state['player2']
        else:
            state['turn'] = state['player1']





@app.route('/')
@cross_origin()
def main_page():
    return jsonify(value='TicTacToe')

def reset_game():
    state['number_of_players'] = 0


def check_if_game_has_been_won():
    if ((game[0] == game[1] == game[2]) and game[0] != 0):
        return True
    elif ((game[3] == game[4] == game[5]) and game[3] != 0):
        return True
    elif ((game[6] == game[7] == game[8]) and game[6] != 0):
        return True
    elif ((game[0] == game[3] == game[6]) and game[0] != 0):
        return True
    elif ((game[1] == game[4] == game[7]) and game[1] != 0):
        return True
    elif ((game[2] == game[5] == game[8]) and game[2] != 0):
        return True
    elif ((game[0] == game[4] == game[8]) and game[0] != 0):
        return True
    elif ((game[2] == game[4] == game[6]) and game[2] != 0):
        return True
    else:
        return False



if __name__ == '__main__':

    app.run()