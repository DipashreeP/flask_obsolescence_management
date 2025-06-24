from flask import Flask, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({"message": "Helloo Folks!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
