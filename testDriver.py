from TempFile import TempFile

if __name__ == '__main__':
    t = TempFile("TestCode/ptest2/in.py")
    t.run()
    t.writeTo("TestCode/ptest2/out.py")
