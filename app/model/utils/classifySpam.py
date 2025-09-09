from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer

clfs = {
    'SVC': load('app/model/trained/svc_model.joblib'),
    'KNN': load('app/model/trained/knn_model.joblib'),
    'NB': load('app/model/trained/nb_model.joblib'),
    'LR': load('app/model/trained/lr_model.joblib'),
    'RF': load('app/model/trained/rf_model.joblib'),
    'Adaboost': load('app/model/trained/adaboost_model.joblib'),
    'Bgc': load('app/model/trained/bgc_model.joblib'),
    'ETC': load('app/model/trained/etc_model.joblib'),
    'GBDT': load('app/model/trained/gbdt_model.joblib'),    
}

vectorizer: TfidfVectorizer = load('app/model/trained/vectorizer.joblib')

def classify_email_spam(email_vector):
    res = 0
    for name, clf in clfs.items():
        res += clf.predict(email_vector)[0]
    return res

def vectorize(email_text):
    return vectorizer.transform([email_text]).toarray()