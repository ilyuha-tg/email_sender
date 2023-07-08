# -*- coding: utf-8 -*-

import pandas as pd
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def main():
    email_name, g_form = get_emails_form_gsheet()
    for email in list(g_form['Email']):
        result = send_email(email, email_name, g_form)
        print(result)


def get_emails_form_gsheet():
    """1 Отримуємо пошти користувачів з гугл документу до якого прив'язана форма
    для цього:
    1) в гугл таблиці відкриваємо доступ по посиланню
    2) sheet_id знаходиться у посиланні між "d/" і наступним "/"
    3) Зберігаємо таблицю у датафреймі
    """
    sheet_id = '1vZww5y3kQzzeXQplrK97EYroe_hzTRUZKhRk8UqICDs'
    g_form = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    email_name = dict(zip(list(g_form['Email']), list(g_form['First Name'])))
    return email_name, g_form


def send_email(email, email_name, g_form):
    sender = "Ведіть Вашу пошту"
    receiver = email
    """Зараз за політикою google НЕ МОЖНА використовувати пароль від пошти
    https://myaccount.google.com/apppasswords - треба зареєструватися тут 
    інший пристрій - ввести назву якусь - отримуєте 16 символів. Вони і будуть паролем
    Ця опція доступна якщо на аккаунті включена двохфактрона верефікація.
    Альтернатива: password = "1234qwert" -Небезпечно але працює
    """
    password = os.environ.get('PASSWORD')
    msg = MIMEMultipart('related')
    name = email_name[email]
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    """
    Тут я припустив, що в гугл таблиці проставлені поступив - не поступив значеннями True і False.
    Відповідно до цього буде обраний шаблон листа
    """
    email_value = g_form['Apply to program'].loc[g_form['Email'] == email].values
    try:
        if email_value == True:
            try:
                 with open('my_letter.html', 'r', encoding='utf-8') as file:
                     text = file.read().format(name=name)
            except IOError:
                return "File does not found"
        elif email_value == False:
            try:
                with open('fail.html', 'r', encoding='utf-8') as file:
                    text = file.read().format(name=name.title())
            except IOError:
                return "File does not found"
        else:
            raise SystemExit("Check info for this email")
    except ValueError:
        raise SystemExit("You have duplicate emails")

    """Бажано в папці з файлами створити папку image і картинки зібрати туди - щоб шляхи не змінювати"""

    msg.attach(MIMEText(text, 'html'))


    with open('image/image001.png', 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name='image001.png')
        image.add_header('Content-ID', '<image001>')
        msg.attach(image)
    with open('image/telegram.png', 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name='telegram.png')
        image.add_header('Content-ID', '<telegram>')
        msg.attach(image)
    with open('image/inst.png', 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name='inst.png')
        image.add_header('Content-ID', '<inst>')
        msg.attach(image)
    with open('image/linkid.png', 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name='linkid.pn')
        image.add_header('Content-ID', '<linkid>')
        msg.attach(image)
    with open('image/fb.png', 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name='fb.png')
        image.add_header('Content-ID', '<fb>')
        msg.attach(image)
    with open('image/youtube.png', 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name='youtube.png')
        image.add_header('Content-ID', '<youtube>')
        msg.attach(image)

    try:
        server.login(sender, password)
        msg["Subject"] = "CLICK ME PLEASE!"
        server.sendmail(sender, receiver, msg.as_string())
        return f"The message was sent to {receiver} successfully!"
    except:
        return f"Incorrect email {receiver}"


if __name__ == "__main__":
    main()


