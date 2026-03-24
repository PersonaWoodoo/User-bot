import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import os

def load_emails():
    emails = []
    if os.path.exists("emails.txt"):
        with open("emails.txt", "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    try:
                        email, password = line.strip().split(maxsplit=1)
                        email = email.strip('"')
                        password = password.strip('"')
                        emails.append((email, password))
                    except ValueError:
                        print(f"Ошибка в строке: {line.strip()}. Пропускаем.")
    return emails

def send_email(sender_email, sender_password, recipient_email, subject, message):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"Ошибка аутентификации: {e}")
        return False
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
        return False

async def anon_command(event):
    try:
        input_text = event.raw_text.replace(".anon", "").strip()
        if not input_text:
            await event.reply("❌ Используйте: .anon [Тема], [Сообщение], [Почта получателя]")
            return

        parts = [part.strip() for part in input_text.split(",", 2)]
        if len(parts) != 3:
            await event.reply("❌ Неверный формат. Используйте: .anon [Тема], [Сообщение], [Почта получателя]")
            return

        subject, message, recipient_email = parts

        emails = load_emails()
        if not emails:
            await event.reply("❌ Нет доступных почт в файле emails.txt.")
            return

        sender_email, sender_password = random.choice(emails)

        if send_email(sender_email, sender_password, recipient_email, subject, message):
            await event.reply(f"✅ Сообщение отправлено с почты: {sender_email}")
        else:
            await event.reply(f"❌ Ошибка при отправке сообщения с почты: {sender_email}\n"
                              f"Убедитесь, что:\n"
                              f"1. Двухфакторная аутентификация включена.\n"
                              f"2. Используется пароль приложения.\n"
                              f"3. Доступ для ненадежных приложений включен.")
    except Exception as e:
        await event.reply(f"🚫 Ошибка: {str(e)}")
