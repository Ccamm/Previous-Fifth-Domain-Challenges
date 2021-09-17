

from flask import Flask, render_template, request
from config import Config

app = Flask(__name__)
app.config.from_object(Config)



@app.route("/")
def home():
    flag = Config.FLAG
    hackername = request.headers.get('Hacker-Name')
    hackers = ["z3r0 c00l","4c1dburn","cr4sh 0v3rr1d3"]
    return render_template("home.html",flag=flag,hackername=hackername,hackers=hackers)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')

