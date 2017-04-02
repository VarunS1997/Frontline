from multiprocessing import Pool
from time import sleep
def PARFOR20(i):
	subresult20 = []
	subresult20.append(("print", repr("Running"), repr(i)))
	subresult20.append(("sleep", repr(3)))
	subresult20.append(("print", repr("Closing"), repr(i)))
	return subresult20
def main():
	p = Pool(4)
	result20 = p.map(PARFOR20, [i for i in range(4)])
	p.close()
	for pendingCalls in result20:
		for pcall in pendingCalls:
			eval(pcall[0])(*[eval(arg) for arg in (pcall[1].split(', '))])
if __name__ == '__main__':
	main()
