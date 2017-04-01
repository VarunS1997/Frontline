from time import sleep
def delay():
    for i in range(4):
        print("Running ", i)
        sleep(3)
        print("Closing ", i)

if __name__ == '__main__':
    delay()
