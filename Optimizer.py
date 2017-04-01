from FileProcessing import ScopeObject
import re

class Optimizer:
    def __init__(self, scopeObject):
    	self.__variable_regex_single = re.compile(r"(?P<variable>(\w|\d|\.|\[|\]|\'|\")+)\s*=\s*(\w|\d|\.|\[|\]|\'|\"|\{|\})+(\n|(\(\s*(\w+\s*,\s*)*(\w)*\s*\)))")
        self.__variable_regex_operators = re.compile(r"(?P<variable>(\w|\d|\.|\[|\]|\'|\")+)\s*=\s*((\w+)[^\W]*\s*[\-\+\*\/]+\s*)+(\w+[\w\d\.\[\]\'\"]*)\n")
        self.__variable_regex_operater_equals = re.compile(r"(?P<variable>(\w|\d|\.|\[|\]|\'|\")+)\s*[\+\-]=\s*.*")
        self.__get_declaration = re.compile(r"\w+\s*=\s*(.+)")
        self.__scopeObject = scopeObject

<<<<<<< HEAD
    def _find_variables(self)-> dict:
=======
    def __find_variables(self)-> list:
>>>>>>> 6c25b6ec16b589efa75e01e5cbddcb7c7c48a7a6
		"""
		returns a list of variable declarations
		"""
		variables = {}
		for each in self.__variables_regex_single.findall(str(self.__scopeObject)):
			variables[each[1]] = each[0]
		for each in self.__variables_regex_operators.findall(str(self.__scopeObject)):
			variables[each[1]] = each[0]
		for each in self.__variables_regex_operator_equals.findall(str(self.__scopeObject)):
			variables[each[1]] = each[0]
		return variables

<<<<<<< HEAD
	def find_constants(self, variables) -> list:
		"""
		Finds constant variables within scope
		"""
		variable_names = variables.keys()
		constants = []
		local = exec(str(self.__scopeObject)).locals()
		for each in variable_names:
			declaration = self.__get_declaration.match(variables[each]).group(1)
			function_args = None
			try:
				function_args = re.match(r"(?P<funcCall>(?P<func>([a-zA-Z]*\.)*[a-zA-Z]+)\((?P<args>[^+\-/*\n]*)\)[ \n])",variables[each]).group('args').split(',')
			except:
				pass
			if re.match(r"\"\w*\"|\d*",declaration) != None:
				constants.append(variables[each])
			if function_args!= None:
				for args in function_args:
					if args not in local:
						constants.append(variables[each])
		return constants:

	def eval_expressions(self):
		"""
		Evaluates expressions within the scope
		"""
		for line in self.__scopeObject():
			try:
				expression = re.match(r"((\d+[\+\-\*\/])+\d+)", str(line)).group(0)
				new_line = str(line)- expression
				new_line = new_line + eval(expression)
				line.replace(new_line)
			except:
				pass
=======
	def __is_localized(self, local: dict) -> bool:
		"""
		Determines weather the variables are local to the loop
		"""
		variables = self.__find_variables()
		for each in variables:
			if each not in local.keys():
				return False
		return True
>>>>>>> 6c25b6ec16b589efa75e01e5cbddcb7c7c48a7a6

	def move_variable_dec(self):
		"""
		Moves the variable to a higher scope if it is constant
		"""
<<<<<<< HEAD
		variables = self._find_variables()
		constants = self.find_constants(variables)
		for each in constants:
			for line in self.scopeObject():
				if each == str(line):
					line.ascend_scope()
=======
		local = exec(str(self.__scopeObject)).locals()
		if not self.__is_localized(local):
			for each in self.__scopeObject:

>>>>>>> 6c25b6ec16b589efa75e01e5cbddcb7c7c48a7a6

    def run(self):
        self.move_variable_dec()
        self.eval_expressions()
