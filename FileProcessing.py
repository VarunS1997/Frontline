class ScopeObject:
	def __init__(self, line: str, scope_type: str, parent):
		''' takes a line of python code and scope type and parent node '''
		self.__line = line
		self.__scopeType = scope_type
		self.__children = []
		self.__parent = parent

	def get_line(self):
		return self.__line

	def __str__(self):
		''' returns the string of the code '''
		string = self.get_line() or ""
		if not self.is_statement():
			for child in self.__children:
				string += str(child)
		return string

	def ascend_scope(self):
		''' moves the requested line to a higher scope if possible, return false if not'''
		if self.is_root():
			return False
		else:
			self.become_child_of(self.__parent.get_parent()

	def become_child_of(self, other):
		other.add_child(self)
		self.__parent.remove_child(self)
		self.__parent = other

	def replace(self, new_line: str):
		''' replace the old lines with the new line '''
		self.__line = new_line

	def __iter__(self):
		''' iterates line by line '''
		if(self.__line != None):
			yield self.__line
		for child in self.__children:
			for line in child:
				yield line

	# THE FOLLLOWING IS TREE PROCESSING, UNNEEDED FOR YOU GUYS
	def add_child(self, new_child, index = None):
		''' inserts another line of code at the specified index (default end) '''
		if(index == None):
			self.__children.append(new_child)
		else:
			self.__children.insert(index, new_child)

		new_child.__parent = self

	def remove_child(self, child):
		self.__children.remove(child)

	def size_of(self):
		''' returns the number of contained lines/scopes '''
		return len(self.__children)

	def get_type(self):
		return self.__scopeType

	def is_statement(self):
		''' returns if this scope object represents a statement '''
		return len(self.__children) == 0

	def is_root(self):
		return self.__parent == None

	def get_parent(self):
		return self.__parent

class TempFile:
	def __init__(self, file_address: str):
		''' Handles file opening and initialization of optimizer and parallelizer and etc'''
		scopeObjPtr = ScopeObject(None, None, None)

		file = open(file_address)
		tabCount = 0

		for line in file:
			cTabs = line.count("\t")
			if(line.rstrip() == ""):
				continue
			elif(cTabs == tabCount + 1): # deeper
				tabCount += 1
				newchild = ScopeObject(line, self.__typeOfScope(line), scopeObjPtr)
				scopeObjPtr.add_child(newchild)
				scopeObjPtr = newchild
			else:
				while tabCount > cTabs: # ascend scopes
					tabCount -= 1
					scopeObjPtr = scopeObjPtr.get_parent()
				newchild = ScopeObject(line, self.__typeOfScope(line), scopeObjPtr)
				scopeObjPtr.add_child(newchild)


		file.close()
		while not scopeObjPtr.is_root():
			scopeObjPtr = scopeObjPtr.get_parent()
		self.__root = scopeObjPtr
		self.__done = False

	def __str__(self):
		'''Calling str(TempFile) returns a string of current file (with modifications)'''
		return str(self.__root)

	def run(self):
		''' Runs the optimizer and the parallelizer by calling their run functions on each scope object in order of ascending scope '''
		pass

	def is_done(self):
		''' returns if the file processing and optimizing is done '''
		return self.__done

	def writeTo(self, root_dir: str):
		''' Write the current file state to the root directory '''
		writefile = open(root_dir, "w")
		writefile.write(str(self))
		writefile.close()

	def get_root(self):
		return self.__root

	def __typeOfScope(self, code: str):
		''' returns the type of scope that the code is '''
		CodeTypes = {"for": "LOOP", "while": "LOOP", "def" : "FUNCTION", "class": "CLASS"}
		for k,v in CodeTypes.items():
			if(code.rstrip().lower().startswith(k)):
				return v
		return "STATEMENT"

	def __iter__(self):
		''' enables for each loop -- a line by line '''
		for line in self.__root:
			yield line

	def __add__(self, other):
		''' combines two files (for parallelization purposes) '''
		if isinstance(other, TempFile):
			for child in other.get_root():
				self.__root.add_child(child)
		elif isinstance(other, ScopeObject):
			self.__root.add_child(other)
