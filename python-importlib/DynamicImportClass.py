import importlib

class DynamicImportClass:
	def load_module_func_with_importlib(module_name):
		mod = importlib.import_module(module_name)
		return mod

	def load_module_func_with_low_level_mothod(module_name):
		mod = __import__('%s' %(module_name), fromlist=[module_name])
		return mod


if __name__ == '__main__':
	test = DynamicImportClass()
	# test