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
    return render_template('index.html')

def generate_board():
    the_board = boggle_game.make_board()
    return the_board

@app.route('/startGame')
def start():
    the_board=generate_board()
    session['board'] = the_board
    return render_template('home.html', the_board=the_board)

@app.route('/check_word')
def check_word():
    the_board =session['board']
    guess = request.args['guess']
   
    # check if it is a valid word
    return jsonify({'result':boggle_game.check_valid_word(the_board, guess)})

@app.route('/more_statistics', methods=["POST"])
def more_stats():
    score=request.json
    print('*from request*')
    print(score)
    print('****')
    print(session)
    if 'score' in session:
        print("****score is in session")
        highest = session['score']
        
    else:
        print("****score is NOT in session")
        session['score'] = 0
        highest=0
    print('*****highest socre in session *******')
    print(highest)
    session['score']=highest
    if highest < score['score']:
        session['score'] = score
    attempts=session.get('attempt',0)
    attempts+=1
    session['attempt']=attempts
    print('***score*****')
    print(session['score'])
    print('***attempt*****')
    print(session['attempt'])
    
    return jsonify(session['score'])