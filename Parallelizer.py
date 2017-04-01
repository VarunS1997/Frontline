from ScopeObject import ScopeObject
import re

class Parallelizer:

    def __init__(self, scopeObject):
        self.__done = False
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
            funcMatch = re.match(r"(?P<funcCall>(?P<func>([a-zA-Z]*\.)*[a-zA-Z]+)\((?P<args>[^+\-/*\n]*)\)[ \n])", line)
            if(funcMatch != None):
                args = funcMatch.group("args").replace(" ", "").split(",")
                if any([arg not in internalVars for arg in args]):
                    self.__scopeObject.get_child(line).replace("subresult" + uniqueId + ".append(({0}, {1}))\n".format(funcMatch.group("func"), tuple(args)))

        loopFuncDec = "def PARFOR" + uniqueId + "(" + varName + "):\n"
        print("REPLACING: " + str(self.__scopeObject.get_line().encode("unicode-escape")))
        self.__scopeObject.replace(loopFuncDec)


    def __parallelize_for_loop(self):
        oldCode = self.__oldCode.strip()
        varName = oldCode.split(" ")[1]
        uniqueId = str(self.__scopeObject.get_id())

        selfIndex = self.__scopeObject.get_parent().index_of(self.__scopeObject)

        self.__scopeObject.get_parent().add_child("\t"*self.__tabCount + "p = Pool(4)\n", selfIndex+1)
        self.__scopeObject.get_parent().add_child("\t"*self.__tabCount + "result" + uniqueId + " = p.map(PARFOR" + uniqueId + ", [" + varName + " " + oldCode.rstrip()[:-1] + "])\n", selfIndex+2)
        self.__scopeObject.get_parent().add_child("\t"*self.__tabCount + "p.close()\n", selfIndex+3)

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
            varMatch = re.match(r"(?P<variable>(\w)+)(\s*)=(\s*)(\w|\.|\'|\")+", line)
            if(varMatch != None):
                variables.insert(varMatch.group("variable"))
        return variables

    def __is_parallizable(self):
        '''
        Checks that the scope object is self-contained
        '''
        pass
