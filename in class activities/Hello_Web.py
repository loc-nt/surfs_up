from flask import Flask

# create a new app Instance (a singular version of something):
app = Flask(__name__)

# Define the starting point , aka the root
@app.route('/') # The forward slash is commonly known as the highest level of hierarchy in any computer system.

def hello_world():
	print("Welcome to my API!")
	return 'Hello baby world!'

@app.route('/aboutme')
def about():
	print('This is run in python only, and will NOT show to the client (or in the browser)')
	return 'I am Loc from Bay Area.'

@app.route('/contact')
def contact():
	return 'My email is abc@bcd.com'

if __name__ == "__main__":
	app.run(debug = True)