from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/handle_login', methods=['POST'])
def handle_login():
    if request.form["username"] == "simon" and request.form["password"] == "safe":
        return "You are logged in Simon"
    else:
        error = "Invalid credentials"
        return render_template("login.html", error=error)



if __name__=="__main__":
    app.run(debug=True)
