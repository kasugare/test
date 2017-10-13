import importlib

class DynamicImportClass:
	def __init__(self):
		print "-" * 50
		print "%s" %"Dynamic import python class".rjust(38)
		print "-" * 50

	def load_module_func_with_importlib(self, module_name):
		mod = importlib.import_module(module_name)
		return mod

	def load_module_func_with_low_level_mothod(self, module_name):
		mod = __import__('%s' %(module_name), fromlist=[module_name])
		return mod


if __name__ == '__main__':
	test = DynamicImportClass()
	userOutterClass = test.load_module_func_with_low_level_mothod("Test")
	userClass = getattr(userOutterClass, "Test")
	test = userClass()
	print "# Step 1 (FUNC):", userOutterClass.printTestFunction()
	print "# Step 2 (CLSS):", test.printTest()