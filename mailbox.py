from imap_tools import MailBox
from imap_tools import OR
import smtplib
import email
from datetime import date
import keyring
import logging

logging.basicConfig(filename='mailbox.log', level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')

Host = 'mail.example.ru'
Users = {
    'name': 'name@example.com'
}


def get_password(*args: str, func='get') -> str:
    """
    work with passwords
    :param args: 'system', 'username', 'password' (if func is 'set')
    :param func: 'set', 'get' (by default)
    :return: password if func is 'get'
    """
    funcs = {
        'set': keyring.set_password,
        'get': keyring.get_password
    }
    password = funcs[func](*args)
    if password is not None:
        return password
    else:
        print('unknown password!')
        username = input('input username: ')
        password = input('input password: ')
        funcs['set']('system', username, password)
        return password


# Get date, subject and body len of all emails from INBOX folder
def get_emails(user):
    with MailBox(Host).login(user, get_password('system', user)) as mailbox:
        for msg in mailbox.fetch(OR(date_gte=date.today())):
            print(msg.date, msg.subject, len(msg.text or msg.html))


def send_emails(user, recipient):
    with smtplib.SMTP_SSL(host=Host, port=2525) as smtp_ssl:

        # Log In to mail account
        password = get_password('system', user)
        resp_code, response = smtp_ssl.login(user=user, password=password)

        print(f"Response Code: {resp_code}")
        print(f"Response     : {response.decode()}")

        # Send Mail
        print("\nSending Mail....")
        message = email.message.EmailMessage()
        message.set_default_type("text/plain")

        message["From"] = user
        message["To"] = recipient
        message["Subject"] = "Еще одно Сообщение"

        body = f'test 03'

        message.set_content(body)

        try:
            response = smtp_ssl.sendmail(from_addr=user,
                                         to_addrs=recipient,
                                         msg=message.as_string())
            print(f'Response: {response}')
        except Exception as ee:
            logging.error(f'Can not send message, reason: {ee}')
