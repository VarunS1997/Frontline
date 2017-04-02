from time import sleep
def factorial(n):
	if n == 1:
		return n
	else:
		return n * factorial(n-1)

def main():
	a = []
	for i in range(20):
		c = factorial(600)
		sleep(0.5) # in place of difficult calculation
		a.append(c-factorial(i+500))
		print(i)
	return a

if __name__ == '__main__':
	main()
