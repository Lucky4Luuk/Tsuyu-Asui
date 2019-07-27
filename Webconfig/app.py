from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main() :
    return "Tsuyu Asui's webconfig (WIP)"

@app.route('/hello')
def hello() :
    return 'Hello, World!'

@app.route("/<id>")
def config(id) :
    return render_template("main.html", id=id)

print("Webconfig booted!")
