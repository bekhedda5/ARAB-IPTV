from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running! 2026"

if __name__ == "__main__":
    app.run()
