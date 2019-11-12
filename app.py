from flask import Flask, request, jsonify
import json
import socket

from random import randrange

app = Flask(__name__)

state = {}
number_of_players = 0
game = [0 for i in range(9)]

id = 0

@app.route('/game', methods = ['GET'])
def foo():

    if number_of_players < 2:
        id += 1
        number_of_players += 1

        if number_of_players == 1:
            state['player1'] = id
        else:
            state['player2'] = id
            state['winner'] = 0

            x = randrange(1, 100)

            if x <= 50:
                state['turn'] = state['player1']
            else:
                state['turn'] = state['player2']


        return jsonify(id = id, status = True)
    else:
        return jsonify(status= False)


@app.route('/heartbeat', methods = ['POST'])
def heartbeat():
    data = json.loads(request.json)
    id = data['id']

    if state['turn'] == id:
        return jsonify(value= True, winner = state['winner'], game=game)
    else:
        return jsonify(value=False)


@app.route('/turn', methods = ['POST'])
def process_turn():
    data = json.loads(request.json)
    move = data['index']
    id = data['id']

    if game[move] != 0:
        return 'hv'
    else:
        game[move] = id 

        if check_if_game_has_been_won():
            state['winner'] = id

        
        if state['turn'] == state['player1']:
            state['turn'] = state['player2']
        else:
            state['turn'] = state['player1']





@app.route('/')
def main_page():
    print('Welcome')


def check_if_game_has_been_won():
    if ((game[0] == game[1] == game[2]) and game[0] != 0) or
    ((game[3] == game[4] == game[5]) and game[3] != 0) or
    ((game[6] == game[7] == game[8]) and game[6] != 0) or
    ((game[0] == game[3] == game[6]) and game[0] != 0) or
    ((game[1] == game[4] == game[7]) and game[1] != 0) or
    ((game[2] == game[5] == game[8]) and game[2] != 0) or
    ((game[0] == game[4] == game[8]) and game[0] != 0) or
    ((game[2] == game[4] == game[6]) and game[2] != 0):
        return True
    else:
        return False



if __name__ == '__main__':

    app.run()