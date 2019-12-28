import pickle
import numpy as np
from sklearn.metrics import accuracy_score
from app.src.spam_classify import (load_email, TEST_DATA)
from app.src.import_data import crawl_data


mnb = pickle.load(open('model.sav', 'rb'))
vectorizer = pickle.load(open('model_vector.sav', 'rb'))
crawl_data(test=True)

test_emails = [email for email in load_email(TEST_DATA)]

X = np.array(test_emails)
Y = np.array([1]*len(test_emails))

X_prepared = vectorizer.transform(X)


result = mnb.predict(X_prepared)
score = accuracy_score(Y, result)
print(score)
