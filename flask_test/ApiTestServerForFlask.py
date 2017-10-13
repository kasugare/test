from flask import Flask

app = Flask(__name__)

class ApiServerTest:

	@app.route('/')
	def hello():
		return "A-Lab ML Framework"

	@app.route('/test')
	def get_test():
		return "test"

	def serverStart(self):
		# app.debug
		app.run()

if __name__ == '__main__':
	server = ApiServerTest()
	# server.debug()
	server.serverStart()
