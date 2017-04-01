from multiprocessing import Pool
def PARFOR38(i):
	subresult38 = []
	subresult38.append(("results.append", repr(i*i)))
	return subresult38
def main():
	results = []
	p = Pool(4)
	result38 = p.map(PARFOR38, [i for i in range(10)])
	p.close()
	for pendingCalls in result38:
		for pcall in pendingCalls:
			eval(pcall[0])(*[eval(arg) for arg in (pcall[1].split(', '))])
	print(results)
	return results
if __name__ == "__main__":
	main()
