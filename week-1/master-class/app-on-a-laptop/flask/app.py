from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from Master Class!</h1>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
