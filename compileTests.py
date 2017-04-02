from TempFile import TempFile
from Analyzer import testCase

ptests = ["ptest1", "ptest2", "ptest3", "ptest4"]
otests = ["otest1"]
allTests = ptests + otests

def compiletests():
	def compile(subdir, parallize = True, optimize = True):
		t = TempFile("TestCode/" + subdir + "/in.py")
		t.set_parallize(parallize)
		t.set_optimize(optimize)
		t.run()
		t.writeTo("TestCode/" + subdir + "/out.py")

	for d in ptests:
		compile(d, True, False)

	for d in otests:
		compile(d, False, True)

if __name__ == '__main__':
	compiletests()
	print("ALL TESTS COMPILED")
	if "y" in input("Run all tests?").lower():
		for i, test in enumerate(allTests):
			print("ANALYZING ", i)
			testCase(test)
