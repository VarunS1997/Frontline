from time import sleep
def main():
    for i in range(4):
        print("Running ", i)
        sleep(1)
        print("Closing ", i)

if __name__ == '__main__':
    main()
