from FileProcessing import ScopeObject

class Translator:
    def __init__(self, scopeObject):
    	self.__scopeObject = scopeObject
    	self.__code_translations = {"sort()": self.merge_sort() }

    def increment_operator(self):
    	"""
		Translates ++  to += 1 and inserts it to the scope
		"""
		pass

	def decrement_operator(self):
		"""
		Translates -- to -=1 and inserts to the scope
		"""
		pass

    def merge_sort(self) -> str:
    	"""
    	Implement merge sort on an unsorted list
    	"""
    	pass

    def translate(self):
    	"""
    	Translates convenient code to legal code
    	"""


    def run(self):
    	pass