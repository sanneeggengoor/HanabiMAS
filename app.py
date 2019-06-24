from flask import Flask, render_template

app = Flask(__name__)

def game():
    return True

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/introduction')
def show_report():
    return render_template('introduction.html')

@app.route('/rules')
def show_rules():
    return render_template('rules.html')

@app.route('/strategy')
def show_strategy():
    return render_template('strategy.html')

@app.route('/logic')
def show_logic():
    return render_template('logic.html')

@app.route('/kripke')
def show_kripke():
    return render_template('kripke.html')

@app.route('/implementation')
def show_implementation():
    return render_template('implementation.html')

@app.route('/result')
def show_result():
    return render_template('result.html')

@app.route('/conclusion')
def show_conclusion():
    return render_template('conclusion.html')

@app.route('/references')
def show_references():
    return render_template('references.html')


if __name__ == '__main__':
    app.run()
