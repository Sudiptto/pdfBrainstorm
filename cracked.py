# app.py
from flask import Flask, render_template

# Create the Flask application
app = Flask(__name__)

# Define a route and its handler
@app.route('/')
def hello():
    return render_template('index.html')

# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
