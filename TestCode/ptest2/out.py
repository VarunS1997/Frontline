from multiprocessing import Pool
from time import sleep
def PARFOR17(i):
	subresult17 = []
	print("Running ", i)
	sleep(3)
	print("Closing ", i)
	return subresult17
def main():
	p = Pool(4)
	result17 = p.map(PARFOR17, [i for i in range(4)])
	p.close()
if __name__ == '__main__':
	main()
