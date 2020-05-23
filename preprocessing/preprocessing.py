# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:51:19 2019

@author: visanand
"""

import pandas as pd

df=pd.read_csv(r"C:\Users\vishal\Desktop\ML\Scrap\youtube_data.csv")
cols=['video_id','Description','transcript','title','category_id','likes','dislikes','views']
df=df[cols]
df=df.dropna(subset=['transcript']) 
df['merged']=df['transcript']+' ' +df['Description'].astype(str)+' '+df['title'].astype(str)

import re
from tqdm import tqdm
tqdm.pandas()
train = df
print("Train shape : ",train.shape)

#removes nan
train['merged']=train['merged'].replace(r'nan', r' ', regex=True)
#removes text inside [], () brackets
train['merged']=train['merged'].replace(r'[\(\[].*?[\)\]]', r' ', regex=True)
#removs text between * * 
train['merged']=train['merged'].replace(r'\*[^*]+\*', r' ', regex=True)
#removing https:\\
train['merged']=train['merged'].replace(r'http\S+', r' ', regex=True)
#removuing www
train['merged']=train['merged'].replace(r'www.\S+', r' ', regex=True)
#removing space case
train['merged']=train['merged'].replace(r'  ', r' ', regex=True)
train['merged']=train['merged'].replace(r'   ', r' ', regex=True)


def build_vocab(sentences, verbose =  True):
    """
    :param sentences: list of list of words
    :return: dictionary of words and their count
    """
    vocab = {}
    for sentence in tqdm(sentences, disable = (not verbose)):
        for word in sentence:
            try:
                vocab[word] += 1
            except KeyError:
                vocab[word] = 1
    return vocab

sentences = train["merged"].progress_apply(lambda x: x.split()).values
vocab = build_vocab(sentences)
print({k: vocab[k] for k in list(vocab)[:5]})

from gensim.models import KeyedVectors

news_path = r'C:\Users\vishal\Desktop\ML\quora\quora-insincere-questions-classification\embeddings\GoogleNews-vectors-negative300\GoogleNews-vectors-negative300.bin'
embeddings_index = KeyedVectors.load_word2vec_format(news_path, binary=True)


import operator 

def check_coverage(vocab,embeddings_index):
    a = {}
    oov = {}
    k = 0
    i = 0
    for word in tqdm(vocab):
        try:
            a[word] = embeddings_index[word]
            k += vocab[word]
        except:

            oov[word] = vocab[word]
            i += vocab[word]
            pass

    print('Found embeddings for {:.2%} of vocab'.format(len(a) / len(vocab)))
    print('Found embeddings for  {:.2%} of all text'.format(k / (k + i)))
    sorted_x = sorted(oov.items(), key=operator.itemgetter(1))[::-1]

    return sorted_x

oov = check_coverage(vocab,embeddings_index)

oov[:10]


def clean_text(x):

    x = str(x)
    for punct in "/-'":
        x = x.replace(punct, ' ')
    for punct in '&':
        x = x.replace(punct, f' {punct} ')
    for punct in '?!.,"#$%\'()*+-/:;<=>@[\\]^_`{|}~' + '“”’':
        x = x.replace(punct, '')
    return x

train["merged"] = train["merged"].progress_apply(lambda x: clean_text(x))
sentences = train["merged"].apply(lambda x: x.split())
vocab = build_vocab(sentences)

oov = check_coverage(vocab,embeddings_index)

oov[:10]

for i in range(10):
    print(embeddings_index.index2entity[i])
    
import re

def clean_numbers(x):

    x = re.sub('[0-9]{5,}', '#####', x)
    x = re.sub('[0-9]{4}', '####', x)
    x = re.sub('[0-9]{3}', '###', x)
    x = re.sub('[0-9]{2}', '##', x)
    return x

train["merged"] = train["merged"].progress_apply(lambda x: clean_numbers(x))
sentences = train["merged"].apply(lambda x: x.split())
vocab = build_vocab(sentences)

oov = check_coverage(vocab,embeddings_index)

oov[:20]

def _get_mispell(mispell_dict):
    mispell_re = re.compile('(%s)' % '|'.join(mispell_dict.keys()))
    return mispell_dict, mispell_re



mispell_dict = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", 
                "could've": "could have", "couldn't": "could not", "didn't": "did not", 
                "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not",
                "haven't": "have not", "he'd": "he would","he'll": "he will", "he's": "he is", 
                "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is", 
                "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have",
                "I'm": "I am", "I've": "I have", "i'd": "i would", "i'd've": "i would have",
                "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have",
                "isn't": "is not", "it'd": "it would", "it'd've": "it would have", "it'll": "it will",
                "it'll've": "it will have","it's": "it is", "let's": "let us", "ma'am": "madam",
                "mayn't": "may not", "might've": "might have","mightn't": "might not",
                "mightn't've": "might not have", "must've": "must have", "mustn't": "must not",
                "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have",
                "o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have",
                "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have",
                "she'd": "she would", "she'd've": "she would have", "she'll": "she will", 
                "she'll've": "she will have", "she's": "she is", "should've": "should have",
                "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have",
                "so's": "so as", "this's": "this is","that'd": "that would", "that'd've": "that would have",
                "that's": "that is", "there'd": "there would", "there'd've": "there would have",
                "there's": "there is", "here's": "here is","they'd": "they would", 
                "they'd've": "they would have", "they'll": "they will", "they'll've": "they will have",
                "they're": "they are", "they've": "they have", "to've": "to have", "wasn't": "was not",
                "we'd": "we would", "we'd've": "we would have", "we'll": "we will", 
                "we'll've": "we will have", "we're": "we are", "we've": "we have", "weren't": "were not",
                "what'll": "what will", "what'll've": "what will have", "what're": "what are", 
                "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have",
                "where'd": "where did", "where's": "where is", "where've": "where have",
                "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have",
                "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not",
                "won't've": "will not have", "would've": "would have", "wouldn't": "would not", 
                "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would",
                "y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",
                "you'd": "you would", "you'd've": "you would have", "you'll": "you will", 
                "you'll've": "you will have", "you're": "you are", "you've": "you have", 'colour': 'color',
                'centre': 'center', 'favourite': 'favorite', 'travelling': 'traveling', 
                'counselling': 'counseling', 'theatre': 'theater', 'cancelled': 'canceled',
                'labour': 'labor', 'organisation': 'organization', 'wwii': 'world war 2',
                'citicise': 'criticize', 'youtu ': 'youtube ', 'Qoura': 'Quora', 'sallary': 'salary', 
                'Whta': 'What', 'narcisist': 'narcissist', 'howdo': 'how do', 'whatare': 'what are',
                'howcan': 'how can', 'howmuch': 'how much', 'howmany': 'how many', 'whydo': 'why do', 
                'doI': 'do I', 'theBest': 'the best', 'howdoes': 'how does', 'mastrubation': 'masturbation',
                'mastrubate': 'masturbate', "mastrubating": 'masturbating', 'pennis': 'penis', 
                'Etherium': 'Ethereum', 'narcissit': 'narcissist', 'bigdata': 'big data', '2k17': '2017', 
                '2k18': '2018', 'qouta': 'quota', 'exboyfriend': 'ex boyfriend', 'airhostess': 'air hostess', 
                "whst": 'what', 'watsapp': 'whatsapp', 'demonitisation': 'demonetization', 
                'demonitization': 'demonetization', 'demonetisation': 'demonetization'}

mispellings, mispellings_re = _get_mispell(mispell_dict)

def replace_typical_misspell(text):
    def replace(match):
        return mispellings[match.group(0)]

    return mispellings_re.sub(replace, text)
#removes any misppelings
    

train["merged"] = train["merged"].progress_apply(lambda x: replace_typical_misspell(x))
sentences = train["merged"].progress_apply(lambda x: x.split())
to_remove = ['a','to','of','and']
sentences = [[word for word in sentence if not word in to_remove] for sentence in tqdm(sentences)]
vocab = build_vocab(sentences)

oov = check_coverage(vocab,embeddings_index)
#train = train.apply(lambda x: x.str.lower())

train.to_csv("preprocessed_youtube_data.csv")

