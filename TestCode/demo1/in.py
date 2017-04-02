from os.path import realpath, dirname
def main():
    result = []
    for fname in ["data1.txt", "data2.txt", "data3.txt", "data4.txt"]:
        f = open(dirname(realpath(__file__)) + "/" + fname, "r")
        s = str(f.read())
        wordli = s.split(" ")
        result.append({w : s.count(w) for w in set(wordli)})
        f.close()
    print(result)

if __name__ == '__main__':
    main()
