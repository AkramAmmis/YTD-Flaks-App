from flask import Flask
from flask import render_template, redirect, url_for, flash, request
from pytube import YouTube
from os import rename


app = Flask(__name__)



from view import view
app.register_blueprint(view)


if __name__ == '__main__' :
    app = create_app()
    app.run_app(debug=True)
