def main():
    result = []
    for fname in ["data1.txt", "data2.txt", "data3.txt", "data4.txt"]:
        f = open(fname, "r")
        a = str(f.read())
        result.append(a.count(" ") > 1000)
        f.close()

if __name__ == '__main__':
    main()
