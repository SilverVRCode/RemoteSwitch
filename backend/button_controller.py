from flask import Flask, request

app = Flask(__name__)

@app.route("/button-press")
def button_press():
    print(request.args.get("button-type"), request.args.get("direction"))
    return "yippee"
