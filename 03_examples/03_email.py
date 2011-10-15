# -*- encoding: utf-8 -*-

import getpass, imaplib

# Соединяемся с почтовым сервером
M = imaplib.IMAP4_SSL("imap.gmail.com", 993)
# Авторизуемся
M.login("fmfprimat@gmail.com", getpass.getpass("Enter password: "))
# Выбираем папку по умолчанию (inbox)
M.select()
# Ищем все письма в папке
typ, data = M.search(None, 'ALL')
# Выводим на экран письма
for num in data[0].split()[:1]: # ограничимся первым письмом
    typ, data = M.fetch(num, '(RFC822)')
    print 'Message %s\n%s\n' % (num, data[0][1])
M.close()
M.logout()
