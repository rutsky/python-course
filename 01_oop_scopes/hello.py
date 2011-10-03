a = 30

def f(arg):
    v = 12
    return locals(), globals()

print "Hello!"

#print "locals: ", f("aaa")[0]
#print "globals:", f("aaa")[1]

#print __file__

def g():
    a = 10
    print a

def g1():
    global a
    a = 10
    print "g1():", a

#print "start a:", a
#g1()
#print "end a:", a

def h1():
   def h2():
       print "h2()"
   return h2

k = h1()
print "k:", k
k()

h1()()

