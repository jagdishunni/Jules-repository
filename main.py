import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World! AI Influencer Intelligence Platform"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
