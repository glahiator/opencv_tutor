from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = "12345678"
bootstrap = Bootstrap(app)

@app.route("/")
def index():
    user_agent = request.headers.get("User-Agent")
    return render_template('index.html')

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)

@app.route("/resp")
def response():
    response = make_response("<h1>Make response</h1>")
    response.status_code = 222
    response.set_cookie("answer", "42")
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
