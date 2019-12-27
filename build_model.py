import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from app.src.spam_classify import (
    HAM_DATA, SPAM_DATA, load_email)


LIMIT = 2000
vectorizer = TfidfVectorizer('english')

ham_emails = [email for email in load_email(HAM_DATA, limit=LIMIT)]
spam_emails = [email for email in load_email(SPAM_DATA, limit=LIMIT)]

X = np.array(ham_emails+spam_emails)
Y = np.array([0]*len(ham_emails)+[1]*len(spam_emails))

X_prepared = vectorizer.fit_transform(X)
X_train, X_test, Y_train, Y_test = train_test_split(
    X_prepared, Y, test_size=0.2, random_state=42)

mnb = MultinomialNB(alpha=.2)
mnb.fit(X_train, Y_train)

pickle.dump(mnb, open('model.sav', 'wb'))
pickle.dump(vectorizer, open('model_vector.sav', 'wb'))
