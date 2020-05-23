# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 10:57:06 2019

@author: ravshukl1
"""

import os
import re

import inflection







def _load_words(words_file):
         with open(words_file, 'r') as f:
             censor_list = [line.strip() for line in f.readlines()]
         return censor_list 


def append_words( word_list,censor_list):
            censor_list.extend(word_list)
            return censor_list
 
 
          
def remove_word(word,censor_list):
        censor_list.remove(word)
    
def is_clean(input_text,censor_list):
        """Returns True if input_text doesn't contain any profane words, False otherwise."""
        return not has_bad_word(input_text,censor_list)
    
def is_profane(input_text,censor_list):
        """Returns True if input_text contains any profane words, False otherwise."""
        return has_bad_word(input_text,censor_list)
def censor(input_text,censor_list):
        """Returns input_text with any profane words censored."""
        bad_words = get_profane_words(censor_list)
        res = input_text

        for word in bad_words:
            # Apply word boundaries to the bad word
            regex_string = r'{0}' if False else r'\b{0}\b'
            regex_string = regex_string.format(word)  
            regex = re.compile(regex_string, re.IGNORECASE)
            censor_char = "*"
            res = regex.sub(censor_char * len(word), res)

        return res
def has_bad_word( text,censor_list):
        """Returns True if text contains profanity, False otherwise."""
        return censor(text,censor_list) != text
def get_profane_words(censor_list):
        """Returns all profane words currently in use."""
        profane_words = []

        if censor_list:
            profane_words = [w for w in censor_list]  # Previous versions of Python don't have list.copy()
       
        

        #profane_words.extend(self._extra_censor_list)
        profane_words.extend([inflection.pluralize(word) for word in profane_words])
        profane_words = list(set(profane_words))
        
        # We sort the list based on decreasing word length so that words like
        # 'fu' aren't substituted before 'fuck' if no_word_boundaries = true
        profane_words.sort(key=len)
        profane_words.reverse()

        return profane_words    
def count_profane(text,censor_list):
     c = 0
     for v in censor_list:
         c = c + text.count(v)
     return c
 
# =============================================================================
# censor_list = []
# censor_list = _load_words(words_file)
#  remove_word('cunt',censor_list) 
# is_profane('Hey! you mean',censor_list)
# count_profane('Hey! fuck you mean cule Assface affucksg abccockbvd',censor_list)
# extend = ['cunt','cule']
# censor_list = append_words( extend,censor_list)
# 
# =============================================================================
