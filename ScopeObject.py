class ScopeObject:
	idCounter = 0
	def __init__(self, line: str, parent):
		''' takes a line of python code and scope type and parent node '''
		self.__line = line
		self.__children = []
		self.__parent = parent
		self.__id = ScopeObject.idCounter

		ScopeObject.idCounter += 1

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
		def remove_ltab(child):
			child.__raw_replace(child.get_line()[1:])
			for subchild in child.get_children():
				remove_ltab(subchild)
		if self.is_root() or self.__parent.is_root():
			return False
		else:
			pindex = self.__parent.get_parent().index_of(self.__parent)
			self.__parent.remove_child(self)
			self.__parent = self.__parent.get_parent()
			self.__parent.add_child(self, pindex)
			remove_ltab(self)


	def refactor(self, old_name, new_name):
		self.__line.replace(old_name, new_name)
		for child in self.__children:
			child.refactor(old_name, new_name)

	def replace(self, new_line: str):
		''' replace the old lines with the new line '''
		self.__line = "\t"*self.__line.count("\t") + new_line

	def __iter__(self):
		''' iterates line by line '''
		if(self.__line != None):
			yield self.__line
		for child in self.__children:
			for line in child:
				yield line

	def get_type(self):
		''' Possible types are FUNCTION LOOP CLASS STATEMENT '''
		return self.__typeOfScope()

	def is_statement(self):
		''' returns if this scope object represents a statement '''
		return len(self.__children) == 0

	# THE FOLLLOWING IS TREE PROCESSING, UNNEEDED FOR YOU GUYS
	def add_child(self, new_child, index = None):
		''' inserts another line of code at the specified index (default end) '''
		if self.get_type() == "STATEMENT":
			return

		if(isinstance(new_child, str)):
			nchild = ScopeObject(new_child, self)
		else:
			nchild = new_child

		if(index == None):
			self.__children.append(nchild)
		else:
			self.__children.insert(index, nchild)

		nchild.__parent = self

	def set_parent(self, other):
		self.__parent = other

	def index_of(self, child):
		for i, c in enumerate(self.__children):
			if child == c:
				return i
		return -1

	def get_child(self, line):
		for child in self.__children:
			if(child.get_line() == line):
				return child

	def get_children(self):
		return self.__children

	def remove_child(self, rchild):
		if(isinstance(rchild, str)):
			for child in self.__children:
				if(child.get_line() == child):
					remove_child(child)
		else:
			self.__children.remove(rchild)

	def get_id(self):
		return self.__id

	def size_of(self):
		''' returns the number of contained lines/scopes '''
		return len(self.__children)

	def is_root(self):
		return self.__parent == None

	def get_parent(self):
		return self.__parent

	def __raw_replace(self, new):
		self.__line = new

	def __eq__(self, other):
		if isinstance(other, ScopeObject):
			return self.__id == other.__id
		else:
			return False

	def __typeOfScope(self):
		''' returns the type of scope that the code is '''
		if(self.__line == None):
			return None
		CodeTypes = {"for": "FORLOOP", "while": "WHILELOOP", "def" : "FUNCTION", "class": "CLASS", "if": "CONDITIONAL", "else": "CONDITIONAL", "elif": "CONDITIONAL"}
		code = self.__line.replace(" ", "").strip().lower()
		for k,v in CodeTypes.items():
			if(code.startswith(k)):
				return v
		return "STATEMENT"
