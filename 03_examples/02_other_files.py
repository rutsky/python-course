# -*- encoding: utf-8 -*-

# Ввод с клавиатуры и вывод на экран в консоли делается также через 
# объекты-файлы:
print "Enter string:"
import sys
string = sys.stdin.readline() # прочитает строку с клавиатуры
# И выведет её в консоль:
sys.stdout.write("You entered: " + string)

# Читать можно не только файлы, но и, например, сайты:
import urllib2
f = urllib2.urlopen("http://school30.spb.ru/cgsg/")
for i in xrange(5):
    print f.readline(),
f.close()
