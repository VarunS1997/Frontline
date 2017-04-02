from TempFile import TempFile
from Analyzer import testCase

ptests = ["ptest1", "ptest2", "ptest3", "ptest4", "demo1"]
otests = ["otest1", "otest2", "otest3", "demo2"]
atests = ["atest1"]
allTests = ptests + otests + atests

def compiletests():
	def compile(subdir, parallize = True, optimize = True):
		t = TempFile(open("TestCode/" + subdir + "/in.py"))
		t.set_parallize(parallize)
		t.set_optimize(optimize)
		t.run()
		t.writeTo("TestCode/" + subdir + "/out.py")

	for d in ptests:
		compile(d, True, False)

	for d in otests:
		compile(d, False, True)

	for d in atests:
		compile(d)

if __name__ == '__main__':
	compiletests()
	print("ALL TESTS COMPILED")
	userin = input("Run all tests?").lower().strip()
	trials = input("Trials?")
	if trials == "":
		trials = 100
	else:
		trials = int(trials)
	fullSpeed = "n" in input("Pauses?").lower().strip()
	outputs = []
	for i, test in enumerate(allTests):
		print("ANALYZING ", i, test)
		if "y" not in userin and userin != "":
			if "y" in input("Skip Test?").lower():
				continue
		try:
			outputs.append(testCase(test, trials).format(i, test))
		except Exception as e:
			print()
			print("TEST FAILURE!!!")
			print(str(e))
			print()
		if not fullSpeed and "q" in input("Press enter to continue, or q to quit").lower():
			break
	final = "TRIALS: " + str(trials) + "\n"
	for output in outputs:
		final += output
		print(output)

	dataFile = open("TestCode/empiricalData.txt", "r")
	data = dataFile.read().split("\n")
	dataFile.close()
	if len(data) <= len(final.split("\n")) or int(data[0].split(" ")[1]) <= trials:
		confirmation = input("OVERWRITE CONFIRM: ").lower()
		if("n" in confirmation or confirmation.strip() == ""):
			print("NO CONFIRMATION. ABORTING SAVE")
		else:
			print("SAVING EMPIRICAL DATA")
			dataFile = open("TestCode/empiricalData.txt", "w")
			dataFile.write(final)
			dataFile.close()
