from multiprocessing import Pool

def f(x):
    a = x
    print("wow")
    return a*x

def simple():
    p = Pool(2)
    print(p.map(f, [i for i in range(5)]))
    p.join()
    p.close()

if __name__ == '__main__':
    simple()
