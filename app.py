from boggle import Boggle
from flask import Flask, request, jsonify, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ohsosecret'
debug=DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False


boggle_game = Boggle()

@app.route('/')
def home():
    the_board=generate_board()
    session['board'] = the_board
    return render_template('home.html', the_board=the_board)

def generate_board():
    the_board = boggle_game.make_board()
    return the_board

@app.route('/check_word', methods=['POST'])
def check_word():
    print('*********')
    print(request.form['guess'])
    guess = request.form['guess']
    if guess in boggle_game.words:
        print('yeah')
        result = "yeah"
    else:
        print('oh nope')
        result = "nope"
    return result