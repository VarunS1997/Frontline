class TempFile:
	def __init__(self, file_address: str):
	''' Handles file opening and initialization of optimizer and parallelizer and etc'''
    pass

	def __del__(self):
	''' cleanup'''
    pass

	def __str__(self):
	'''Calling str(TempFile) returns a string of current file (with modifications)'''
    pass

	def run(self):
	''' Runs the optimizer and the parallelizer by calling their run functions on each scope object in order of ascending scope '''
    pass

	def is_done(self):
	''' returns if the file processing and optimizing is done '''
    pass

	def get(self, line: int):
	'''gets the requested line'''
    pass

	def replace(self, old: ScopeObject, new: ScopeObject):
	''' replaces the code specified by one object with code specified by the 2nd '''
    pass

	def writeTo(self, root_dir: str):
	''' Write the current file state to the root directory '''
	pass

	def __iter__(self):
	''' enables for each loop -- a line by line '''
    pass

	def __add__(self, other: TempFile):
	''' combines two files (for parallelization purposes) '''
	pass

class ScopeObject:
	def __init__(self, lines: str, scope: str):
	''' takes a string of python code and scope '''
    pass

	def list(self):
	''' returns the lines as a list (call like obj.list())'''
    pass

	def __str__(self):
	''' returns the string of the lines '''
    pass

	def replace_line(self, old: str, new: str):
	''' replace a line with a new line '''
    pass

	def ascend_scope(self, var_name: str):
	''' moves the requested variable to a higher scope if possible, return false if not'''
    pass

	def replace(self, old_lines: str, new_lines: str):
	''' replace the old lines with the new lines '''
    pass
