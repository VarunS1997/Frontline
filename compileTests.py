from TempFile import TempFile

def compiletests():
	def compile(subdir, parallize = True, optimize = True):
		t = TempFile("TestCode/" + subdir + "/in.py")
		t.set_parallize(parallize)
		t.set_optimize(optimize)
		t.run()
		t.writeTo("TestCode/" + subdir + "/out.py")

	for d in ["ptest1", "ptest2", "ptest3"]:
		compile(d, True, False)

	for d in ["otest1"]:
		compile(d, False, True)

if __name__ == '__main__':
	compiletests()
	print("ALL TESTS COMPILED")
