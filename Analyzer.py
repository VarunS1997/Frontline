from time import time
import importlib.util
import os
import sys

class Analyzer:
	def __init__(self, subdir):
		self.__main = __import__(subdir, globals(), locals(), ["main"]).main
		self.__elapsedTime = None
		self.__failure = None

	def test(self):
		try:
			pretime = time()
			self.__main()
			self.__elapsedTime = time() - pretime
		except Exception as e:
			self.__failure = True
			print(str(e))

	def get_time(self):
		return self.__elapsedTime

	def get_failure(self):
		return self.__failure

class MassAnalyzer:
	def __init__(self, test_dir):
		self.__analyzer = Analyzer(test_dir)

		self.__times = []

		self.__ready = True
		self.__done = False
		self.__processed = False

		self.__data = None

	def start(self, tests = 100):
		if not self.__ready:
			return
		for a in range(tests):
			self.__analyzer.test()
			self.__times.append(self.__analyzer.get_time())
		self.__ready = False
		self.__done = True

	def get_data(self):
		if self.__done and not self.__processed:
			self.__data = dict()

			totalTime = sum(self.__times)
			totalSuccess = len(self.__times)

			self.__data["TotalTime"] = totalTime
			self.__data["AverageTime"] = totalTime / totalSuccess
			self.__data["Trials"] = totalSuccess
			self.__processed = True
		return self.__data

def testCase(strin, trials):
	normal = MassAnalyzer("TestCode." + strin + ".in")
	optimal = MassAnalyzer("TestCode." + strin + ".out")

	normal.start(trials)
	optimal.start(trials)

	nResults = normal.get_data()
	oResults = optimal.get_data()

	result = ""
	result += "="*20 + "\n"
	result += "RESULTS: TEST {0} '{1}'" + "\n"
	result += "="*20 + "\n"
	result += "TOTAL TIME: " + str(nResults["TotalTime"]) + "="*3 + ">" + str(oResults["TotalTime"]) + "="*3 + ">" + "% Improvement: " + str(round((nResults["TotalTime"]-oResults["TotalTime"])/nResults["TotalTime"], 3)) + "\n"
	result += "AVERAGE TIME: " + str(nResults["AverageTime"]) + "="*3 + ">" + str(oResults["AverageTime"]) + "="*3 + ">" + "% Improvement: " + str(round((nResults["AverageTime"]-oResults["AverageTime"])/nResults["AverageTime"], 3)) + "\n"
	result += "TRIALS: " + str(nResults["Trials"]) + "="*3 + ">" + str(oResults["Trials"]) + "\n"
	result += "="*20 + "\n"
	result += "="*20 + "\n"
	return result

if __name__ == '__main__':
	strin = input("Which TestCode Dir?")
	testCase(strin)
