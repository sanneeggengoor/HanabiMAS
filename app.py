from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
import pandas as pd

app = Flask(__name__)

def game():
    return True

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/kripke')
def showTable():
    return render_template('kripke.html')


if __name__ == '__main__':
    app.run()
