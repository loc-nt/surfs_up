from flask import Flask

# create a new app Instance (a singular version of something):
app = Flask(__name__)

# Define the starting point , aka the root
@app.route('/') # The forward slash is commonly known as the highest level of hierarchy in any computer system.

def hello_world():
	return 'Hello world'