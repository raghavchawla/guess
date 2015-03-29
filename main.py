
import webapp2
import os
import logging
import jinja2
import random
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


mvi=""
hw=""
ntf=""
wa=0
cg = []
flag=True
movie=""
endgame=False


def Main():
    global movie
    global endgame
    global mvi
    global hw
    global ntf
    global wa
    global cg
    endgame=False
    cg=[]
    ntf = "Guess a Character"
    wa=0
    movies = ["Birdman", "Whiplash", "Foxcatcher", "Kingsman"]
    movie=random.choice(movies).upper()
    mvi=""
    for c in movie:
        mvi+="_ "
    hw = "HOLLYWOOD"


class MainHandler(webapp2.RequestHandler):
    def get(self):
        global flag
        if flag:
            Main()
            flag=False
        title="Hello World"
        template_values = {
            'abc':title,
            'mvi':mvi,
            'hw':hw,
            'ntf':ntf
        }

        template = JINJA_ENVIRONMENT.get_template('web/index.html')
        self.response.write(template.render(template_values))
        

def getguess(x):
    if x.isalpha() == False:
        global ntf
        ntf="Enter an alphabet"
        return False
    elif len(x)>1:
        ntf="Enter one alphabet"
        return False
    else:
        return True

    
def inword(b,d):
    for a in b:
        if a==d:
            return True
    return False


def init(b,d):
    global mvi
    mvi=""
    for a in b:
        word=False
        for c in d:
            if c==a:
                word=True
        if word:
            mvi+=a+" "
        else:
            mvi+="_ "


def showstat(d):
    i = 0
    global hw
    hw=""
    b = ['H','O','L','L','Y','W','O','O','D']
    for a in b:
        if i<d:
            i = i+1
            hw+="/"
        else:
            hw+=a

            
def checkwin(b,d):
    for a in b:
        check=True
        for c in d:
            if a==c:
                check=False
        if check==True:
            return False
    return True    


    
class CharGuess(webapp2.RequestHandler):
    def post(self):
        global cg
        global movie
        global ntf
        global wa
        global endgame
        guess = self.request.get('content').upper()
        if not endgame:
             if getguess(guess):
                if inword(movie,guess):
                    cg.append(guess)
                    ntf = "Correct guess"
                    init(movie,cg)
                else:
                    wa=wa+1
                    ntf="Incorrect guess"
                    showstat(wa)
                    if wa == 9:
                        ntf="Game Over, the correct answer was "+movie
                        endgame=True
                if checkwin(movie,cg):
                    ntf="Congrats, you've won! Click Reset to guess one more!"
                    endgame=True
        else:
            ntf="Click Reset to Start"
        self.redirect('/')



class Reset(webapp2.RequestHandler):
    def post(self):
        global flag
        flag=True
        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/guess', CharGuess),
    ('/reset', Reset)
], debug=True)
