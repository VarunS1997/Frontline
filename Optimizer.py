from ScopeObject import ScopeObject
import re

class Optimizer:
	def __init__(self, scopeObject):
		self.__variable_regex_single = re.compile(r"((?P<variable>(\w|\d|\.|\[|\]|\'|\")+)\s*=\s*(\w|\d|\.|\'|\")+(\n|(\(\s*(\w+\s*,\s*)*(\w)*\s*\))))")
		self.__variable_regex_operators = re.compile(r"((?P<variable>(\w|\d|\.|\[|\]|\'|\")+)\s*=\s*((\w+)[^\W]*\s*[\-\+\*\/]+\s*)+(\w+[\w\d\.\[\]\'\"]*)\n)")
		self.__variable_regex_operater_equals = re.compile(r"((?P<variable>(\w|\d|\.|\[|\]|\'|\")+)\s*[\+\-]=\s*.*)")
		self.__variable_regex_structures = re.compile(r"((.+)\s*=\s*[\[\{].*[\]\}])")
		self.__variable_regex_functions = re.compile(r"(?P<funcCall>(?P<func>([a-zA-Z]*\.)*[a-zA-Z]+)\((?P<args>[^+\-/*\n]*)\)[ \n])")
		self.__get_declaration = re.compile(r"\w+\s*=\s*(.+)")
		self.__get_string_addition = re.compile(r"(([\'\"]\w+[\'\"]\s*\+\s*)+[\'\"]\w+[\'\"])")
		self.__get_string_multiplication = re.compile(r"([\"\']\w+[\"\']|\d+)\s*\*\s*([\"\']\w+[\"\']|\d+)")
		self.__get_int_eval = re.compile(r"((\d+[\+\-\*\/])+\d+)")
		self.__get_float_eval = re.compile(r"((\d+.\d+\s*[\+\/\*\-]\s*)+\d+.\d+)")
		self.__get_both_eval = re.compile(r"((\d+\.*\d*\s*\+\s*)+\d+)")
		self.__list_of_evals = [self.__get_string_multiplication, self.__get_string_addition, self.__get_int_eval, self.__get_float_eval, self.__get_both_eval]
		self.__scopeObject = scopeObject

	def __find_variables(self)-> dict:

		"""
		returns a dict of the variables and their declarations
		"""
		variables = {}
		for each in self.__variable_regex_operater_equals.findall(str(self.__scopeObject)):
			variables[each[1]] = each[0]+ "\n"
		for each in self.__variable_regex_single.findall(str(self.__scopeObject)):
			variables[each[1]] = each[0]
		for each in self.__variable_regex_operators.findall(str(self.__scopeObject)):
			variables[each[1]] = each[0]

		return variables

	def __find_data_structures(self) -> dict:
		"""
		Finds things like dictionaries and lists and returns them as a dictionary
		"""
		variables = {}
		for each in self.__variable_regex_structures.findall(str(self.__scopeObject)):
			variables[each[1].strip()] = each[0].strip()
		return variables

	def __find_function_calls(self) -> dict:
		"""
		Finds function calls and returns them in a dictionary
		"""
		variables = {}
		for each in self.__variable_regex_functions.findall(str(self.__scopeObject)):
			variables[each[2][:len(each[2])-1]] = each[0]
		return variables

	def find_constants(self, variables) -> list:
		"""
		Finds constant variables within scope
		"""
		variable_names = variables.keys()
		constants = []
		local = self.__find_localized_variables()
		for each in variable_names:
			declaration = ''
			try:
				declaration = self.__get_declaration.match(variables[each]).group(1)
			except:
				pass
			if re.match(r"\"\w*\"|\d*",declaration) != None:
				constants.append(variables[each])
		return constants

	def eval_expressions(self):
		"""
		Evaluates all expressions within the scope
		"""
		for line in self.__scopeObject.get_children():
			for regex in self.__list_of_evals:
				try:
					expression = None
					if regex == self.__get_int_eval:
						expression = regex.findall(str(line).strip())[0][0]
					if regex == self.__get_string_multiplication:
						expression = [regex.findall(str(line).strip())[0][0],regex.findall(str(line).strip())[0][1]]
						expression = '*'.join(expression)
					if regex == self.__get_string_addition:
						expression = regex.findall(str(line).strip())[0][0]
					if regex == self.__get_float_eval:
						expression = regex.findall(str(line).strip())[0][0]
					if regex == self.__get_both_eval:
						expression = regex.findall(str(line).strip())[0][0]
					new_line = list(str(line))
					for each in list(expression):
						new_line.remove(each)
					new_line = ''.join(new_line) + str(eval(''.join(expression)))
					line.replace(" ".join(new_line.split())  + "\n")
				except:
					pass


	def move_variable_dec(self):
		"""
		Moves the variable to a higher scope if it is constant
		"""
		variables = self.__find_variables()
		constants = self.find_constants(variables)
		print(constants)
		for each in constants:
			for line in self.__scopeObject.get_children():
				if each == str(line).strip()+"\n":
					line.ascend_scope()

	def move_data_structure_dec(self):
		"""
		Moves a data structure to a higher scope if it is not mutated within the scope
		"""
		data = self.__find_data_structures()
		functions = self.__find_function_calls()
		if data != {} and functions != {}:
			for each in data.keys():
				if each not in functions.keys():
					for line in self.__scopeObject.get_children():
						if each == str(line).strip() +"\n":
							line.ascend_scope()
		elif data != {}:
			for each in data.keys():
				for line in self.__scopeObject.get_children():
					if data[each] == str(line).strip():
						line.ascend_scope()

	def __find_localized_variables(self)-> list:
		"""
        returns a list of variable declarations
        """
		variables = set()
		for line in self.__scopeObject:
			varMatch = re.match(r"(?P<variable>(\w)+)(\s*)=(\s*)(\w|\.|\'|\")+", line)
			if(varMatch != None):
				variables.insert(varMatch.group("variable"))
		return variables

	def empty_loop(self):
		"""
		Gets rid of empty loops
		"""
		if re.findall(r"(for)", self.__scopeObject.get_line()) != []:
			if self.__scopeObject.get_children() == []:
				self.__scopeObject.get_parent().remove_child(self.__scopeObject)

	def keep_useful_code(self):
		pass

	def run(self):
		self.eval_expressions()
		self.move_variable_dec()
		self.move_data_structure_dec()
		self.move_variable_dec()
		self.empty_loop()




