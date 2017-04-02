from ScopeObject import ScopeObject
import re
import keyword
import builtins

class Parallelizer:

    def __init__(self, scopeObject, processes = 4):
        self.__done = False
        self.__processes = processes
        self.__parallelized = False
        self.__scopeObject = scopeObject
        self.__tabCount = self.__scopeObject.get_line().count("\t")
        self.__oldCode = self.__scopeObject.get_line()

    def run(self):
        scopeType = self.__scopeObject.get_type()
        print("PROCESSING TYPE " + self.__scopeObject.get_type() + " : " + str(self.__scopeObject.get_line().encode("unicode-escape")))
        if(scopeType != None):
            if(scopeType not in ["FUNCTION", "FORLOOP"]):
                self.__done = True
                return
            elif(scopeType == "FORLOOP"):
                self.__prep_for_loop()
                self.__parallelize_for_loop()
                self.__parallelized = True

    def has_parallelized(self):
        return self.__parallelized

    def __prep_for_loop(self):
        """
        Makes the for loop contain a subresult variable which will be the return value and will contain a list of tuples to call (func, args)
        """
        uniqueId = str(self.__scopeObject.get_id())
        varName = self.__scopeObject.get_line().rstrip().split(" ")[1]

        self.__scopeObject.add_child("\t"*(self.__tabCount+1) + "subresult" + uniqueId + " = []\n", 0)
        self.__scopeObject.add_child("\t"*(self.__tabCount+1) + "return subresult" + uniqueId + "\n")

        internalVars = self.__find_localized_variables()
        for line in self.__scopeObject:
            print("FOR LOOP CHECK: ", str(line.encode("unicode-escape")))
            funcMatch = re.match(r"(?P<funcCall>(?P<func>([a-zA-Z]*\.)*[a-zA-Z]+)\((?P<args>[^\n]*)\)[ \n]?)", line.strip())
            assignMatch = re.match(r"(?P<variable>[^\[]+)\[(?P<arg1>[^\]]+)\] *= *(?P<arg2>[^\n]+)", line.strip())
            if(funcMatch != None):
                args = re.split(", *", funcMatch.group("args"))

                basis = funcMatch.group("func")
                basis = basis[:basis.index(".") if "." in basis else len(basis)]
                print("INTERNVAL VARS: ", internalVars)
                if any([(re.match(r"(?P<open>[\"\']).*(?P=open)", var) == None and re.match(r"[0-9]+", var) == None) and var not in internalVars for var in args]) and not (basis in internalVars or basis in dir(builtins) or keyword.iskeyword(basis)):
                    print("BASIS: ", basis, basis == "print", "print" in dir(builtins))
                    self.__scopeObject.get_child(line).replace("subresult" + uniqueId + ".append(({0}, tuple([{1}])))\n".format('"{}"'.format(funcMatch.group("func")), ", ".join(["repr({})".format(arg) for arg in args])))
            elif(assignMatch != None):
                var = assignMatch.group("variable")
                arg1 = assignMatch.group("arg1")
                arg2 = assignMatch.group("arg2")
                if var not in internalVars:
                    self.__scopeObject.get_child(line).replace("subresult" + uniqueId + ".append(({0}, tuple([{1}])))\n".format('"{0}.__setitem__"'.format(var), ", ".join(["repr({})".format(arg) for arg in [arg1, arg2]])))
        loopFuncDec = "def PARFOR" + uniqueId + "(" + varName + "):\n"
        print("REPLACING: " + str(self.__scopeObject.get_line().encode("unicode-escape")))
        self.__scopeObject.replace(loopFuncDec)


    def __parallelize_for_loop(self):
        oldCode = self.__oldCode.strip()
        varName = oldCode.split(" ")[1]
        uniqueId = str(self.__scopeObject.get_id())

        selfIndex = self.__scopeObject.get_parent().index_of(self.__scopeObject)

        self.__scopeObject.get_parent().add_child("\t"*self.__tabCount + "p = Pool(" + str(self.__processes) + ")\n", selfIndex+1)
        self.__scopeObject.get_parent().add_child("\t"*self.__tabCount + "result" + uniqueId + " = p.map(PARFOR" + uniqueId + ", [" + varName + " " + oldCode.rstrip()[:-1] + "])\n", selfIndex+2)
        self.__scopeObject.get_parent().add_child("\t"*self.__tabCount + "p.close()\n", selfIndex+3)

        compilationForLoopObj = ScopeObject("\t"*self.__tabCount + "for pendingCalls in result" + uniqueId + ":\n", self.__scopeObject.get_parent())
        compilationForLoopObj.add_child("\t"*(self.__tabCount+1) + "for pcall in pendingCalls:\n")
        compilationForLoopObj.get_children()[0].add_child("\t"*(self.__tabCount+2) + "eval(pcall[0])(*[eval(arg) for arg in pcall[1]])\n")
        self.__scopeObject.get_parent().add_child(compilationForLoopObj, selfIndex+4)

        ptr = self.__scopeObject.get_parent()
        while(not ptr.is_root()):
            ptr = ptr.get_parent()
            self.__scopeObject.ascend_scope()

    def __find_localized_variables(self)-> list:
        """
        returns a list of variable declarations
        """
        variables = set()
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

        return variables

    def __is_parallel_recursion(self):
        '''
        Checks that the function is recursive and branching
        '''
        pass
