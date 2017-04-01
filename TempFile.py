from Parallelizer import Parallelizer
from Optimizer import Optimizer
from ScopeObject import ScopeObject

class TempFile:
	def __init__(self, file_address: str):
		''' Handles file opening and initialization of optimizer and parallelizer and etc'''
		scopeObjPtr = ScopeObject(None, None)

		file = open(file_address)
		tabCount = 0

		for line in file:
			fline = line.replace("    ", "\t")
			cTabs = fline.count("\t")
			print("READING: ", fline.encode("unicode-escape"))
			print("CTABS: ", cTabs, " === tabCount: ", tabCount)
			if(line.rstrip() == ""):
				continue
			elif(cTabs == tabCount + 1): # deeper
				tabCount += 1
				scopeObjPtr = scopeObjPtr.get_children()[-1]
				newchild = ScopeObject(fline, scopeObjPtr)
				scopeObjPtr.add_child(newchild)
			else:
				while tabCount > cTabs: # ascend scopes
					tabCount -= 1
					scopeObjPtr = scopeObjPtr.get_parent()
				newchild = ScopeObject(fline, scopeObjPtr)
				scopeObjPtr.add_child(newchild)

		file.close()
		while not scopeObjPtr.is_root():
			scopeObjPtr = scopeObjPtr.get_parent()
		self.__root = scopeObjPtr
		self.__done = False
		self.__parallelImports = False
		self.__parallelize = True
		self.__optimize = True

	def __str__(self):
		'''Calling str(TempFile) returns a string of current file (with modifications)'''
		return str(self.__root)

	def set_parallize(self, b):
		self.__parallelize = b

	def set_optimize(self, b):
		self.__optimize = b

	def run(self):
		''' Runs the optimizer and the parallelizer by calling their run functions on each scope object in order of ascending scope '''
		if(self.__optimize):
			self.__run__optimizer()
		if(self.__parallelize):
			self.__run_parallizer()

	def __run_parallizer(self):
		def run_subroutine(child):
			for subchild in child.get_children():
				run_subroutine(subchild)
			p = Parallelizer(child)
			p.run()
			if(not self.__parallelImports and p.has_parallelized()):
				self.__parallelImports = True
				self.__root.add_child("from multiprocessing import Pool\n", 0)

		childrenList = list(self.__root.get_children())
		for child in childrenList:
			run_subroutine(child)

	def __run__optimizer(self):
		def run_subroutine(child):
			for subchild in child.get_children():
				run_subroutine(subchild)
			o = Optimizer(child)
			o.run()

		childrenList = list(self.__root.get_children())
		for child in childrenList:
			run_subroutine(child)

	def is_done(self):
		''' returns if the file processing and optimizing is done '''
		return self.__done

	def writeTo(self, root_dir: str):
		''' Write the current file state to the root directory '''
		writefile = open(root_dir, "w")
		writefile.write(str(self))
		writefile.close()
		print("="*20)
		print("FULL WRITING:")
		print("="*20)
		print(str(self.__root))
		print("="*20)

	def get_root(self):
		return self.__root

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
