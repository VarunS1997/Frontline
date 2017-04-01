from multiprocessing import Pool
def PARFOR2(i):
	subresult2 = []
	a = 4 + 2
	print("Running ", i)
	return subresult2
def main():
	p = Pool(4)
	result2 = p.map(PARFOR2, [i for i in range(5)])
	p.close()
	return 2
if __name__ == '__main__':
	main()
