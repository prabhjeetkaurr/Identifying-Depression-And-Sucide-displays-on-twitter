from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib

import warnings
warnings.filterwarnings("ignore")



tweets = pd.read_csv('train_data_flag.csv',
                     header=None,
                     skiprows=1,
                     names=["name","id","description","friends","followers","location","tweet","flag"])


tweets.loc[(tweets['flag'] == 1) , ['flag']] = 'DEPRESSED'
tweets.loc[(tweets['flag'] == 0) , ['flag']] = 'NORMAL'

features=tweets['tweet']
labels=tweets['flag']

x_train,x_test,y_train,y_test=train_test_split(features, labels, test_size=0.2, random_state=42)

tfidf_vectorizer=TfidfVectorizer(stop_words='english', max_df=0.7)
tfidf_vectorizer.fit(x_train)
tfidf_train=tfidf_vectorizer.transform(x_train)
tfidf_test=tfidf_vectorizer.transform(x_test)

pa_classifier=PassiveAggressiveClassifier(max_iter=50)
pa_classifier.fit(tfidf_train,y_train)

y_pred=pa_classifier.predict(tfidf_test)
score=accuracy_score(y_test,y_pred)
print(f'Accuracy: {round(score*100,2)}%')

#Save Model
joblib.dump(tfidf_vectorizer,"tfidf_vectorizer.pkl")
joblib.dump(pa_classifier, "pa_classifier.pkl")