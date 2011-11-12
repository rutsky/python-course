# -*- encoding: utf-8 -*-
import sys
try:
    # <Блок кода>
    f = open('myfile.txt')
    s = f.readline()
    v = float(s.strip())
    r1 = 1 / int(v)
    r2 = v**v
    
# <ТипИсключения> as <Объект-Исключение>
except IOError as exc:  
    errno, strerror = exc
    print "I/O error({0}): {1}".format(errno, strerror)
except ValueError:
    print "Could not convert data to an integer."
# Обработчик для нескольких исключений
except ZeroDivisionError, OverflowError:
    print "Floating point operation exception."
# Обработчик для всех типов исключений
except:
    # В sys можно найти всю информацию об исключении, включая
    # стек вызовов.
    print "Unexpected error:", sys.exc_info()[0]
    raise   # Оставляем текущее исключение необработанным --- произойдёт поиск 
            # обработчика в следующем вложенном try: ... except: ... 
# Блок, который выполняется если не произошло никакого (непойманного в 
# <блоке кода>) исключения.
else:
    print "No exceptions!"
