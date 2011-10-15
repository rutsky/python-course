# -*- encoding: utf-8 -*-

# Открыть файл на чтение:
f = open("input_file.txt", "rt") # можно также открывать в бинарном режиме: "rb"

# Прочитать первые 10 символов из файла, `first10' --- строка:
first10 = f.read(10) 
print "First 10 chars: '{0}'".format(first10)
# all_file = f.read() --- прочитает файл до конца в строку `all_file'

# Прочитать строку:
str2 = f.readline()
print "String: '{0}'".format(str2)
# all_strings = f.readlines() --- прочитает все строки и вернёт список строк

for line in f:
    # Пройтись по всем оставшимся строкам файла.
    # На каждой итерации в `line' будет очередная строка файла
    print "Line: '{0}'".format(line)

# После окончания работы с файлом его необходимо закрыть:
f.close()
