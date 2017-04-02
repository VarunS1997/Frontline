
def factorial(n):
	if n == 1:
		return n
	else:
		return n * factorial(n-1)

def main():
	a = []
	for i in range(100):
		c = factorial(500)
		a.append(c-i)
	print(a)
	return a

if __name__ == '__main__':
	main()
