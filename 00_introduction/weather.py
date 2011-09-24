# coding: utf-8

from urllib2 import urlopen

# Открываем URL на чтение.
u = urlopen("http://pogoda.yandex.ru/saint-petersburg/")

s = 0 # суммарная длина строк
for line in u:          # читаем u по строкам
    
