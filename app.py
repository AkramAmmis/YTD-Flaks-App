from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY']='DOWN-YT00'

from view import view
app.register_blueprint(view)


if __name__ == '__main__' :
   
    app.run(debug=True)


