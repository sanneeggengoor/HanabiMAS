from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
import pandas as pd
from gameloop import *

app = Flask(__name__)

def game():
    return True

@app.route("/")
def main():
    manager = Game(5,4,5)
    print (manager.playerlist)
    manager.deal_initial()
    manager.print_player_info()
    manager.play_game()
    return render_template('index.html',
                           manager=manager)

@app.route('/kripke')
def showTable():
    return render_template('kripke.html')


if __name__ == '__main__':
    app.run()
