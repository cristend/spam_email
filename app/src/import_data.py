import os
import hashlib
import email
import email.parser
import email.policy
from app.src.email_transform import Transformer

PATH = os.getcwd()
END_PATH = 'app/email_source'
email_to_word = Transformer(stemming=True)


def save_file(data, file_name, directory):
    md5 = hashlib.md5((file_name).encode())
    file_name = md5.hexdigest()

    with open('app/data/{0}/{1}'.format(directory, file_name),
              'w') as f:
        f.writelines(data)
        f.close()


def crawl_data(test=False):
    if test:
        directories = ['test']
    else:
        directories = ['ham', 'spam']
    for directory in directories:
        count = 0
        for path, subdirs, files in os.walk(os.path.join(PATH,
                                                         END_PATH, directory)):
            for name in files:
                file_name = os.path.join(path, name)
                with open(file_name, 'rb') as f:
                    email_item = email.parser.BytesParser(
                        policy=email.policy.default).parse(f)
                    data = email_to_word.transform(email_item)
                    f.close()

                save_file(data, file_name, directory)
                count += 1
        print(count)
