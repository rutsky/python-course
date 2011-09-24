from turtle import *

setup (width=200, height=200, startx=0, starty=0)

#speed ("fastest") # important! turtle is intolerably slow otherwise
#tracer (False)    # This too: rendering the 'turtle' wastes time

for i in range(200):
    forward(i)
    right(90.5)

done()
