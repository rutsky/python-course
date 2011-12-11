def g(func):
    print "g({0})".format(func)
    def wrapper(a, b):
        print "wrapper!"
        func(a, b)
        print "end of wrapper"

    return wrapper

@g
def f(a, b):
    print "f({0}, {1})".format(a, b)

#def f_impl(a, b):
#    print "f({0}, {1})".format(a, b)

#f = f_impl
#f = g(f_impl)

f(3, 0)
f(40, 50)

