def f():
    a = 1
    class C(object):
        g = a
        def f(self):
            print a
    return C()

c = f()
c.f()

