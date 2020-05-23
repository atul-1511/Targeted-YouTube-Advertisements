# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 17:34:38 2019

@author: visanand
"""

import profanity as pf
import pandas as pd
#getting the word file
words_file = r'C:\Users\vishal\Desktop\ML\labelling\bad_words.txt'
censor_list = []
censor_list = pf._load_words(words_file)

df=pd.read_csv(r"C:\Users\vishal\Desktop\ML\preprocessing\preprocessed_youtube_data.csv").drop(["Unnamed: 0"],axis=1)

#marking videos as threat or non threat based on occurance of threat words in the text data
for index ,row in df.iterrows():
    x = pf.count_profane(row[8],censor_list)
    words = len(row[8].split())
    #print(str(x)+" "+str(words))
    if(words>0 and x/words > 0.018):
        df.loc[index,'label'] = [1]
    else:
        df.loc[index,'label'] = [0]

df.to_csv("labelled_processed_youtube_data.csv")
        
        