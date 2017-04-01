from multiprocessing import Pool
from time import sleep
def PARFOR3(i):
	subresult3 = []
	print("Running ", i)
	sleep(3)
	print("Closing ", i)
	return subresult3
def delay():
	p = Pool(4)
	result3 = p.map(PARFOR3, [i for i in range(4)])
	p.close()
if __name__ == '__main__':
	delay()
