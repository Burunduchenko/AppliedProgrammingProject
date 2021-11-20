__version__ = '0.1.0'

from flask import Flask, Response
from waitress import serve

from auth import auth
from user import user
from audience import audience
from reservation import reservation

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(audience)
app.register_blueprint(reservation)


@app.route('/api/v1/hello-world-7')
def myendpoint():
    status_code = Response(response="Hello World 7")
    return status_code


serve(app, host='127.0.0.1', port=8089, threads=1)
