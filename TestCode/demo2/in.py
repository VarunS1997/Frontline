
def factorial(n):
	if n == 1:
		return n
	else:
		return n * factorial(n-1)
a = []
def main():
	for i in range(100):
		c = factorial(100)
		a.append(c-i)
		
if __name__ == '__main__':
	main()

