import argparse

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def show_interface():
    return render_template('hello.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    app.debug = parser.parse_args().debug

    app.run()
