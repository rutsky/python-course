class Record:
    def __init__(self, value):
        print "Record.__init__(" + str(self) + ")"

        self.name = "Peter"
        self.val = value

    def h(self, a, b):
        print "Hello,", self.name, self.val
        print "a =", a, "b =", b

def h1(rec):
    print "1 Hello,", rec.name, rec.val

r1 = Record(1234)
r2 = Record(30)

#r2.h1 = h1
#r2.h1()
#r1.h(30, 40)

