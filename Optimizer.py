from ScopeObject import ScopeObject
import re

class Optimizer:
	def __init__(self, scopeObject):
		self.__variable_regex_single = re.compile(r"((?P<variable>(\w|\d|\.|\[|\]|\'|\")+)\s*=\s*(\w|\d|\.|\'|\")+(\n|(\(\s*(\w+\s*,\s*)*(\w)*\s*\))))")
		self.__variable_regex_operators = re.compile(r"((?P<variable>(\w|\d|\.|\[|\]|\'|\")+)\s*=\s*((\w+)[^\W]*\s*[\-\+\*\/]+\s*)+(\w+[\w\d\.\[\]\'\"]*)\n)")
		self.__variable_regex_operater_equals = re.compile(r"((?P<variable>(\w|\d|\.|\[|\]|\'|\")+)\s*[\+\-]=\s*.*)")
		self.__variable_regex_structures = re.compile(r"((.+)\s*=\s*[\[\{].*[\]\}])")
		self.__variable_regex_functions = re.compile(r"(?P<funcCall>(?P<func>([a-zA-Z]*\.)*[a-zA-Z]+)\((?P<args>[^+\-/*\n]*)\)[ \n])")
		self.__variable_regex_functions2 = re.compile(r"(\w+\s*=\s*(\w+\((?P<args>.*)\)))")
		self.__find_variables = [self.__variable_regex_single, self.__variable_regex_functions, self.__variable_regex_operators, self.__variable_regex_structures,self.__variable_regex_functions2]
		self.__get_declaration = re.compile(r"(\w+)\s*=\s*(.+)")
		self.__get_string_addition = re.compile(r"(([\'\"]\w+[\'\"]\s*\+\s*)+[\'\"]\w+[\'\"])")
		self.__get_string_multiplication = re.compile(r"([\"\']\w+[\"\']|\d+)\s*\*\s*([\"\']\w+[\"\']|\d+)")
		self.__get_int_eval = re.compile(r"((\d+[\+\-\*\/])+\d+)")
		self.__get_float_eval = re.compile(r"((\d+.\d+\s*[\+\/\*\-]\s*)+\d+.\d+)")
		self.__get_both_eval = re.compile(r"((\d+\.*\d*\s*\+\s*)+\d+)")
		self.__list_of_evals = [self.__get_string_multiplication, self.__get_string_addition, self.__get_int_eval, self.__get_float_eval, self.__get_both_eval]
		self.__scopeObject = scopeObject

	def find_variables(self)-> list:

		"""
		returns a list of the variables and their declarations
		"""
		variables = []
		for each in self.__scopeObject.get_children():
			for regex in self.__find_variables:
				variable = regex.findall(str(each))
				if  variable != []:
					variables.append(variable[0][0])
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
		constants = []
		print(variables)
		local = self.__find_localized_variables()
		for each in variables:
			if each[-1] == ']':
				is_constant = False
				for j in variables:
					try:
						if self.__get_declaration.match(each.strip()).group(0) + '.' == self.__variable_regex_functions.match(j).group(3):
							is_constant = True
						else:
							print("hi")
							is_constant = False
							break
					except:
						is_constant = True
				if is_constant:
					constants.append(each)
			elif self.__variable_regex_functions.match(each) == None and self.__variable_regex_functions2.match(each) == None:
				declaration = ''
				try:
					declaration = self.__get_declaration.match(each).group(0)
				except:
					pass
				if re.match(r"\"\w*\"|\d*",declaration) != None:
					constants.append(each)
			else:
				print(each)
				try:
					args = self.__variable_regex_functions.match(each).group("args")
				except:
					args = self.__variable_regex_functions2.match(each).group("args")
				args = args.split(',')
				print(args)
				is_constant = True
				for i in args:
					print(i in local)
					if i in local:
						is_constant = False
				for j in variables:
					try:
						if self.__get_declaration.match(j.strip()).group(0) + '.' == self.__variable_regex_functions.match(each).group(3):
							is_constant = True
						else:
							print("hi")
							is_constant = False
							break
					except:
						pass
				if is_constant:
					constants.append(each)

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
		variables = self.find_variables()
		constants = self.find_constants(variables)
		for each in constants:
			for line in self.__scopeObject.get_children():
				if each.strip() == str(line).strip():
					line.ascend_scope()

	# def is_structure_constant(self, move_data_structure_dec):
	# 	"""
	# 	Moves a data structure to a higher scope if it is not mutated within the scope
	# 	"""
	# 	functions = self.__find_function_calls()
	# 	if data != {} and functions != {}:
	# 		for each in data.keys():
	# 			if each not in functions.keys():
	# 				for line in self.__scopeObject.get_children():
	# 					if each == str(line).strip() +"\n":
	# 						return True:
	# 	elif data != {}:
	# 		for each in data.keys():
	# 			for line in self.__scopeObject.get_children():
	# 				if data[each] == str(line).strip():
	# 					return True:

	def __find_localized_variables(self)-> list:
		"""
        returns a list of variable declarations
        """
		variables = set()
		variables.add("self")
		for line in self.__scopeObject:
			varMatch = re.match(r"(?P<variable>(\w)+)(\s*)=(\s*)(\w|\.|\'|\")+", line.strip())
			defMatch = re.match(r"def [a-zA-z][a-zA-Z0-9]*\((?P<args>[^\)]*)\):", line.strip())
			forMatch = re.match(r"for (?P<var>[a-zA-z][a-zA-z0-9]*) in [^:\]]*", line.strip())
			if(varMatch != None):
				variables.add(varMatch.group("variable"))
			elif(defMatch != None):
				for var in re.split(", *", defMatch.group("args")):
					variables.add(var)
			elif(forMatch != None):
				variables.add(forMatch.group("var"))

		ptr = self.__scopeObject.get_parent()
		while not ptr.is_root():
			ptr = ptr.get_parent()
		for child in ptr.get_children():
			if child.get_type() == "STATEMENT":
				varMatch = re.match(r"(?P<variable>(\w)+)(\s*)=(\s*)(\w|\.|\'|\")+", child.get_line().strip())
				importMatch = re.match(r"from [a-zA-z0-9.]* import (?P<variable>[a-zA-z0-9]*)", child.get_line().strip())
				if varMatch != None:
 					variables.add(varMatch.group("variable"))
				elif importMatch != None:
					variables.add(importMatch.group("variable"))
			elif child.get_type() == "FUNCTION":
				funcMatch = re.match(r"def (?P<func>[a-zA-z][a-zA-Z0-9]*)\([^\)]*\):", child.get_line().strip())
				if funcMatch != None:
					variables.add(funcMatch.group("func"))

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
		if self.__scopeObject.get_type() == 'FORLOOP' and self.__scopeObject.get_parent().get_type() == 'FUNCTION':
			self.move_variable_dec()
			#self.move_data_structure_dec()
			#self.move_variable_dec()
			self.empty_loop()
		




