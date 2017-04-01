from ScopeObject import ScopeObject
import re

class Optimizer:
	def __init__(self, scopeObject):
		self.__variable_regex_single = re.compile(r"(?P<variable>(\w|\d|\.|\[|\]|\'|\")+)\s*=\s*(\w|\d|\.|\[|\]|\'|\"|\{|\})+(\n|(\(\s*(\w+\s*,\s*)*(\w)*\s*\)))")
		self.__variable_regex_operators = re.compile(r"(?P<variable>(\w|\d|\.|\[|\]|\'|\")+)\s*=\s*((\w+)[^\W]*\s*[\-\+\*\/]+\s*)+(\w+[\w\d\.\[\]\'\"]*)\n")
		self.__variable_regex_operater_equals = re.compile(r"(?P<variable>(\w|\d|\.|\[|\]|\'|\")+)\s*[\+\-]=\s*.*")
		self.__get_declaration = re.compile(r"\w+\s*=\s*(.+)")
		self.__get_string_addition = re.compile(r"([\'\"]\w+[\'\"]\s*\+\s*)+[\'\"]\w+[\'\"]")
		self.__get_string_multiplication = re.compile(r"([\"\']\w+[\"\']|\d+)\s*\*\s*([\"\']\w+[\"\']|\d+)")
		self.__get_int_eval = re.compile(r"((\d+[\+\-\*\/])+\d+)")
		self.__get_float_eval = re.compile(r"(\d+.\d+\s*[\+\/\*\-]\s*)+\d+.\d+")
		self.__list_of_evals = [self.__get_string_multiplication, self.__get_string_addition, self.__get_int_eval, self.__get_float_eval]
		self.__scopeObject = scopeObject

	def __find_variables(self)-> dict:

		"""
		returns a dict of the variables and their declarations
		"""
		variables = {}
		for each in self.__variable_regex_single.findall(str(self.__scopeObject)):
			variables[each[1]] = each[0]
		for each in self.__variable_regex_single.findall(str(self.__scopeObject)):
			variables[each[1]] = each[0]
		for each in self.__variable_regex_single.findall(str(self.__scopeObject)):
			variables[each[1]] = each[0]
		return variables


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
		return constants

	def eval_expressions(self, regex):
		"""
		Evaluates all expressions within the scope
		"""
		for line in self.__scopeObject:
			for regex in self.__list_of_evals:
				try:
					expression = regex.match(str(line)).group(0)
					new_line = list(str(line))
					for each in list(expression):
						new_line.remove(each)
					new_line = ''.join(new_line)+ eval(expression)
					line.replace(new_line)
				except:
					pass


	def move_variable_dec(self):
		"""
		Moves the variable to a higher scope if it is constant
		"""
		variables = self.__find_variables()
		constants = self.find_constants(variables)
		for each in constants:
			for line in self.scopeObject():
				if each == str(line):
					line.ascend_scope()

	def run(self):
		self.move_variable_dec()
		self.eval_expressions()
