from multiprocessing import Pool
def PARFOR2(i):
	subresult2 = []
	a = 4 + 2
	subresult2.append(("print", repr("Running"), repr(i)))
	return subresult2
def main():
	p = Pool(4)
	result2 = p.map(PARFOR2, [i for i in range(5)])
	p.close()
	for pendingCalls in result2:
		for pcall in pendingCalls:
			eval(pcall[0])(*[eval(arg) for arg in (pcall[1].split(', '))])
	return 2
if __name__ == '__main__':
	main()
