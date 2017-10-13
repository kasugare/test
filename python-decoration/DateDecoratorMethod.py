import datetime

def datetime_decorator(func):
	def decorated():
		print "Step 1", datetime.datetime.now()
		func()
		print "Step 2", datetime.datetime.now(), "\n"
	return decorated()

@datetime_decorator
def main_function_1():
	print "- MAIN FUNCTION 1 START"

@datetime_decorator
def main_function_2():
	print "- MAIN FUNCTION 2 START"

@datetime_decorator
def main_function_3():
	print "- MAIN FUNCTION 3 START"
