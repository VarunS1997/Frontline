from FileProcessing import ScopeObject
import re

class Optimizer:
    def __init__(self, scopeObject):
    	self.__variable_regex = re.compile(r"(?P<variable>(\w|\d|\.)+)(\s?)=(\s?)(\w|\d|\.|\'|\")+")
        self.__scopeObject = scopeObject

    def __find_variables(self)-> list:
		"""
		returns a list of variable declarations
		"""
		variables = []
		for each in self.__variables_regex.findall(str(self.__scopeObject)):
			variables.append(each[1])
		return variables

	def __is_localized(self, local: dict) -> bool:
		"""
		Determines weather the variables are local to the loop
		"""
		variables = self.__find_variables()
		for each in variables:
			if each not in local.keys():
				return False
		return True

	def move_variable_dec(self):
		"""
		Moves the variable to a higher scope if it is not optimized
		"""
		local = exec(str(self.__scopeObject)).locals()
		if not self.__is_localized(local):
			for each in self.__scopeObject:


    def run(self):
        pass
