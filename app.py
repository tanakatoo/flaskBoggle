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
    """
    displays the beginnnig of the game with a start button
    """
    return render_template('index.html')


@app.route('/startGame')
def start():
    """
    make the board, save it to a session and display on screen
    """
    the_board=boggle_game.make_board()
    session['board'] = the_board
    return render_template('home.html', the_board=the_board)

@app.route('/check_word')
def check_word():
    """
    takes the user's guess and checks to see if it is valid
    returns the result:
    "ok", "not-a-word", "not-on-board"
    """
    the_board =session['board']
    guess = request.args['guess']
   
    # check if it is a valid word
    return jsonify({'result':boggle_game.check_valid_word(the_board, guess)})

@app.route('/more_statistics', methods=["POST"])
def more_stats():
    """
    saves the highest score and how many times they played the game 
    returns the highest score
    """
    score=request.json['score']
    
    if session.get('score',0) < score :
        
        session['score']=score
    
    attempts=session.get('attempt',0)
    attempts+=1
    session['attempt']=attempts
  
    return jsonify(session['score'])