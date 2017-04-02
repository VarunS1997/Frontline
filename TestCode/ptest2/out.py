from multiprocessing import Pool
from time import sleep
def PARFOR20(i):
	subresult20 = []
	print("Running ", i)
	sleep(3)
	print("Closing ", i)
	return subresult20
def main():
	p = Pool(4)
	result20 = p.map(PARFOR20, [i for i in range(4)])
	p.close()
	for pendingCalls in result20:
		for pcall in pendingCalls:
			eval(pcall[0])(*[eval(arg) for arg in pcall[1]])
if __name__ == '__main__':
	main()
