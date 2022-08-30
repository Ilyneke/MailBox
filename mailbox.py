from imap_tools import MailBox
from imap_tools import A, OR
from datetime import date
import keyring


def get_password(*args: str, func='get'):
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
    return funcs[func](*args)


today = date.today()  # today's date...

imapHost = 'mail.example.ru'
imapUser = 'mail@example.com'

# Get date, subject and body len of all emails from INBOX folder
with MailBox(imapHost).login(imapUser, get_password('system', imapUser)) as mailbox:
    for msg in mailbox.fetch(OR(date_gte=today)):
        print(msg.date, msg.subject, len(msg.text or msg.html))
