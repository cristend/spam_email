import os
import re
import random
import email
import email.parser
import email.policy
from collections import Counter
from html import unescape

SOURCE_PATH = 'app/email_source'
DATA_PATH = 'app/data'
HAM_DIR = os.path.join(SOURCE_PATH, 'ham')
SPAM_DIR = os.path.join(SOURCE_PATH, 'spam')
TEST_DIR = os.path.join(SOURCE_PATH, 'test')
HAM_DATA = os.path.join(DATA_PATH, 'ham')
SPAM_DATA = os.path.join(DATA_PATH, 'spam')
TEST_DATA = os.path.join(DATA_PATH, 'test')


def load_email(data_path, limit=None):
    data = list()
    if limit is None:
        for name in os.listdir(data_path):
            with open(os.path.join(data_path, name), 'r') as f:
                data.append(f.read())
            f.close()
        return data
    else:
        for index in range(limit):
            name = random.choice(os.listdir(data_path))
            with open(os.path.join(data_path, name), 'r') as f:
                data.append(f.read())
            f.close()
        return data


def get_email_structure(email_):
    if isinstance(email_, str):
        return email_
    payload = email_.get_payload()

    if isinstance(payload, list):
        return 'multipart({})'.format(','.join([
            get_email_structure(sub_email)
            for sub_email in payload
        ]))
    else:
        return email.get_content_type()


def structures_counter(emails):
    structures = Counter()
    for item in emails:
        structure = get_email_structure(item)
        structures[structure] += 1
    return structures


def html_to_plain_text(html):
    text = re.sub('<head.*?>.*?</head>', '', html, flags=re.M | re.S | re.I)
    text = re.sub(r'<a\s.*?>', ' HYPERLINK ', text, flags=re.M | re.S | re.I)
    text = re.sub('<.*?>', '', text, flags=re.M | re.S)
    text = re.sub(r'(\s*\n)+', '\n', text, flags=re.M | re.S)

    return unescape(text)


def email_to_text(email_):
    html = None

    for part in email_.walk():
        ctype = part.get_content_type()

        if "text/plain" not in ctype and "text/html" not in ctype:
            continue
        try:
            content = part.get_content()
        except Exception:
            content = str(part.get_payload())
        if "text/plain" in ctype:
            content = html_to_plain_text(content)
            return content
        if "text/html" in ctype:
            html = content
    if html:
        return html_to_plain_text(html)
