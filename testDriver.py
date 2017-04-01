from TempFile import TempFile

if __name__ == '__main__':
    t = TempFile("TestCode/otest1/in.py")
    t.run()
    t.writeTo("TestCode/otest1/out.py")
