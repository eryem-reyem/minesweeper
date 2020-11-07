import uuid
from flask import Flask, url_for, request, render_template, session
import game

#export FLASK_ENV=development

app = Flask(__name__)

app.secret_key = b'yuCie4naengaiquoimio'

all_boards = {}

@app.route("/",)
def index():
    if not 'user_id' in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template('game_index.html',  instruction='Play minesweeper? Please ENTER!')

@app.route("/game_start", methods=['POST'])
def game_start():
    level = int(request.form["level"])
    if level == 0:
        board = all_boards[session['user_id']] = game.Game(5,5,3)
    elif level == 1:
        board = all_boards[session['user_id']] = game.Game(13,13,13)
    else:
        board = all_boards[session['user_id']] = game.Game(20,20,60)
    board.set_cellinformations()
    return render_template('game_start.html', width=board.width, height=board.height, board=board.board, coordinates=board.coordinates)  

@app.route("/game_play", methods=['POST'])
def game_play():
    board = all_boards[session['user_id']]
    ainput = request.form['name']
    set_flag = int(request.form["set_flag"])
    coordinate = ainput.split('|')
    if set_flag == 0:
        game_status = board.uncover((int(coordinate[0])+1, int(coordinate[1])+1))
    elif set_flag == 1:
        game_status = board.set_flag((int(coordinate[0])+1, int(coordinate[1])+1))
    else:
        game_status = board.unset_flag((int(coordinate[0])+1, int(coordinate[1])+1))
    return render_template('game_play.html' , ainput=ainput, set_flag=set_flag, width=board.width, 
    height=board.height, board=board.board, coordinates=board.coordinates, game_status=game_status) 

@app.route("/win")
def win():
    return render_template('win.html')

@app.route("/game_over")
def game_index():
    return render_template('game_over.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
