# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 16:58:18 2019

@author: visanand
"""

#import profanity as pf
import os
import pandas as pd

#words_file =r'C:\Users\vishal\Desktop\ML\labelling\bad_words.txt'

#censor_list = []
#censor_list = pf._load_words(words_file)


df = pd.read_csv(r"C:\Users\vishal\Desktop\ML\labelling\labelled_processed_youtube_data.csv" )
#df['merged']=df['transcript'].fillna(df['Description'].fillna(df['title']))
#df=df.dropna(subset=['merged'])
df['merged'] = df['merged'].fillna('').apply(lambda x: x.lower())
#df["merged"]=df["merged"].fillna(" ")
# =============================================================================
# max=0
# count=0
# =============================================================================
import pandas as pd
import gc

#importing machine learning models
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold,train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import log_loss,confusion_matrix,classification_report,roc_curve,auc,accuracy_score
max_features=50


#splitting, creating vectors and then predicting the results
X_train, X_test, y_train, y_test = train_test_split(
df['merged'], df['label'], test_size=0.2, random_state=42)
vectorizer = TfidfVectorizer(max_features=max_features)
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)
LR = LogisticRegression()
LR.fit(X_train, y_train)
y = LR.predict_proba(X_test)[:, 1]

#classifying based on threshold
for j in range(len(y)):
    if( y[j] > 0.5 ):
        y[j] = 1
    else:
        y[j] = 0

#printing the accuracy
print("accuracy for = "+str(accuracy_score(y_test, y)))
