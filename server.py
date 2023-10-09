from flask import Flask
import config

app = Flask(__name__)

patch = config.PATCH

def parse(file):
    with open(file) as file:
        data = file.read()
    return data

@app.route("/")
def hello():
    global patch
    return parse(patch)
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
