from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
		return 'Hello 205CDE!'

if __name__ == '__main__':
		app.debug = True
		app.run(host="0.0.0.0", port=8000)

from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/admin')
def hello_admin():
		return 'Hello Admin'

@app.route("/guest/<guest>")
def hello_guest(guest):
		return 'Hello %s as Guest' % guest	

@app.route("/user/<name>")
def hello_user(name):
		if name == 'admin':
				return redirect(url_for('hello_admin'))
		else:
				return redirect(url_for('hello_guest', guest = name))

if __name__ == '__main__':
		app.debug = True
		app.run(host="0.0.0.0", port=8000)			


