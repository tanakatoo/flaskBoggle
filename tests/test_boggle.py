from app import app
from unittest import TestCase
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS']=['dont-show-debug-toolbar']

class displayHome(TestCase):
    def test_home(self):
        with app.test_client() as client:
            res=client.get('/')
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('<button>START</button>', html)
            # self.assertIn('board',session)

class displayGame(TestCase):
    def test_game(self):
        with app.test_client() as client:
            res=client.get('/startGame')
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('<p id="highestScore">', html)
            self.assertIn('<table>', html)

class checkNotOnBoard(TestCase):
    def test_not_on_board(self):
        with app.test_client() as client:
            guess = 'not'
            the_board=[['X', 'G', 'Q', 'F', 'R'], ['E', 'X', 'F', 'Z', 'B'], ['U', 'C', 'H', 'C', 'Y'], ['V', 'X', 'V', 'G', 'C'], ['B', 'I', 'Q', 'L', 'C']]
            with client.session_transaction() as sess:
                sess['board']=the_board
            res=client.get('/check_word?guess=not')
            # html = res.get_data(as_text=True)
            # self.assertEqual(res.status_code,200)
            self.assertIn(res.json['result'],'not-on-board')
            
class checkNotValid(TestCase):
    def test_not_valid(self):
        with app.test_client() as client:
            guess = 'not'
            the_board=[['X', 'G', 'Q', 'F', 'R'], ['E', 'X', 'F', 'Z', 'B'], ['U', 'C', 'H', 'C', 'Y'], ['V', 'X', 'V', 'G', 'C'], ['B', 'I', 'Q', 'L', 'C']]
            with client.session_transaction() as sess:
                sess['board']=the_board
            res=client.get('/check_word?guess=ajsdkfdfd')
            # html = res.get_data(as_text=True)
            # self.assertEqual(res.status_code,200)
            self.assertIn(res.json['result'],'not-word')

class checkValidWord(TestCase):
    def test_valid_word(self):
        with app.test_client() as client:
            guess = 'not'
            the_board=[['X', 'G', 'Q', 'F', 'R'], 
                       ['E', 'X', 'F', 'Z', 'B'], 
                       ['Y', 'C', 'H', 'C', 'Y'], 
                       ['U', 'X', 'V', 'G', 'C'], 
                       ['B', 'I', 'Q', 'L', 'C']]
            with client.session_transaction() as sess:
                sess['board']=the_board
            res=client.get('/check_word?guess=buy')
            # html = res.get_data(as_text=True)
            # self.assertEqual(res.status_code,200)
            self.assertIn(res.json['result'],'ok')

class more_statistics(TestCase):
     def test_more_stats(self):
        with app.test_client() as client:
            score = 9
            with client.session_transaction() as sess:
                sess['score']=7
                sess['attempt']=3
            res=client.post('/more_statistics', data={'score': score})
            html = res.get_data(as_text=True)
            # self.assertEqual(res.status_code,200)
            self.assertEqual(session['attempt'],4)
            self.assertEqual(session['score'],9)
            