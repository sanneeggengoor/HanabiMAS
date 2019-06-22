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
    return render_template('index.html')

@app.route('/kripke')
def show_models():
    manager = Game(5,4,5)
    print (manager.playerlist)
    manager.deal_initial()
    manager.print_player_info()
    manager.play_game()
    return render_template('kripke.html',
                           manager=manager)

@app.route('/introduction')
def show_report():
    return render_template('introduction.html')

@app.route('/rules')
def show_rules():
    return render_template('rules.html')

@app.route('/strategy')
def show_strategy():
    return render_template('strategy.html')

if __name__ == '__main__':
    app.run()
