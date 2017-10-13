import datetime

class DatetimeDecorator:
	def __init__(self, f):
		self.func = f

	def __call__(self, *args, **kwargs):
		print "\n", datetime.datetime.now()
		self.func(*args, **kwargs)
		print datetime.datetime.now(), "\n"

class MainClass:
	def main_function_1(self):
		print "- MAIN FUNCTION 1 START"

	@DatetimeDecorator
	def main_function_2():
		print "- MAIN FUNCTION 2 START"

	def main_function_3(self):
		print "- MAIN FUNCTION 3 START"

if __name__=='__main__':
	main = MainClass()
	main.main_function_1()
	main.main_function_2()
	main.main_function_3()