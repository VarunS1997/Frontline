from time import time
import sys

class Analyzer:
	def __init__(self, main_py):
		f = open(main_py)
		self.__main = f.read()
		f.close()

		self.__elapsedTime = None
		self.__spaceSize = None
		self.__failure = None

	def test(self):
		try:
			exec(self.__main, globals())

			now = time()
			main()
			self.__elapsedTime = time() - now

			self.__failure = False
		except Exception as e:
			print(e)
			self.__failure = True

	def get_time(self):
		return self.__elapsedTime

	def get_space(self):
		return self.__spaceSize

	def get_failure(self):
		return self.__failure
