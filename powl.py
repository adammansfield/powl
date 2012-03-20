import imaplib
import email
import re
import sys
from optparse import OptionParser

## Copy these into a file name config.py to use
#email_username = "default@gmail.com"
#email_password = "1234"
#email_mailbox = "INBOX"

#try:
#    from config import *
#except ImportError:
#    sys.exit()
    
#imap = imaplib.IMAP4_SSL("imap.gmail.com")
#imap.login(email_username, email_password)
#imap.select(email_mailbox)
#search_response, email_id_list = imap.search(None, "(Unseen)")

#for email_id in email_id_list[0].split():
#    response, data = imap.fetch(email_id, "(RFC822)")
#    mail = email.message_from_string(data[0][1])
    
#    for part in mail.walk():
#        if part.get_content_type() == 'text/html':
#            body = part.get_payload()
    
#    # parses a koodo to email sms message
#    if (body):
#        result = re.split("<center><p><br><p>", body)
#        result = re.split("<p>\r\n</center>", result[1])
#        print result[0]

#imap.close()
#imap.logout()

def transaction(debit, credit, amount, memo):
    print(debit)

def main():
    parser = OptionParser()
    parser.add_option("--transaction")
    parser.add_option("-d", type="string", dest="debit", default="")
    parser.add_option("-c", type="string", dest="credit", default="")
    parser.add_option("-a", type="string", dest="amount", default="")
    parser.add_option("-m", type="string", dest="memo", default="")
    (options, args) = parser.parse_args()
    transaction(options.debit, options.credit, options.amount, options.memo)
    
if __name__ == '__main__':
    main()
