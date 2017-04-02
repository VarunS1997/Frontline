from multiprocessing import Pool
def PARFOR56(i):
	subresult56 = []
	subresult56.append(("results.__setitem__", tuple([repr(i), repr(i*i)])))
	return subresult56
def main():
	results = dict()
	p = Pool(4)
	result56 = p.map(PARFOR56, [i for i in range(10)])
	p.close()
	for pendingCalls in result56:
		for pcall in pendingCalls:
			eval(pcall[0])(*[eval(arg) for arg in pcall[1]])
	print(results)
	return results
if __name__ == "__main__":
	main()
