from time import time
import sys

class Analyzer:
	def __init__(self, main_py):
		f = open(main_py)
		self.__main = f.read()
		f.close()

		self.__elapsedTime = None
		self.__failure = None

		self.__ready = True

	def test(self):
		if not self.__ready:
			return
		try:
			exec(self.__main, globals())

			now = time()
			main()
			self.__elapsedTime = time() - now

			self.__failure = False
			self.__ready = False
		except Exception as e:
			print(e)
			self.__failure = True

	def get_time(self):
		return self.__elapsedTime

	def get_failure(self):
		return self.__failure

class MassAnalyzer:
	def __init__(self, main_py, tests = 100):
		self.__analyzers = []
		for i in range(tests):
			self.__analyzers.append(Analyzer(main_py))
		self.__ready = True
		self.__done = False
		self.__processed = False

		self.__data = None

	def start(self):
		if not self.__ready:
			return
		for a in self.__analyzers:
			a.test()
		self.__ready = False
		self.__done = True

	def get_data(self):
		if self.__done and not self.__processed:
			self.__data = dict()

			totalTime = 0
			totalSuccess = 0

			for a in self.__analyzers:
				if(a.get_failure() == False):
					totalTime += a.get_time()
					totalSuccess += 1

			self.__data["TotalTime"] = totalTime
			self.__data["AverageTime"] = totalTime / totalSuccess
			self.__data["Trials"] = totalSuccess
			self.__processed = True
		return self.__data

def testCase(strin):
	normal = MassAnalyzer("TestCode/" + strin + "/in.py")
	optimal = MassAnalyzer("TestCode/" + strin + "/out.py")

	normal.start()
	optimal.start()

	print("RESULTS:")
	nResults = normal.get_data()
	oResults = optimal.get_data()
	print("TOTAL TIME: ", nResults["TotalTime"], "="*20 + ">", oResults["TotalTime"])
	print("AVERAGE TIME: ", nResults["AverageTime"], "="*20 + ">", oResults["AverageTime"])
	print("TRIALS: ", nResults["Trials"], "="*20 + ">", oResults["Trials"])

if __name__ == '__main__':
	strin = input("Which TestCode Dir?")
	testCase(strin)
