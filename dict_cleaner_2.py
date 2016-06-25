# -*- coding: utf-8 -*-

import nltk
from nltk.corpus import stopwords
import pymorphy2
import pandas as pd
import re
from collections import Counter

def str_key (_dict):
    key = (str(list(_dict.keys())).strip('[]')).replace("'",'')
    return(key)
def str_value (_dict): 
    value = (str(list(_dict.values())).strip('[]')).replace("'",'')
    return(value)

stop_words = stopwords.words('russian')
stop_words.extend(["тка","ка","например", "также", "нибудь", "который", "свой", "обычно", "некоторый", "кому"])
morph = pymorphy2.MorphAnalyzer()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def dict_to_wordlist(text, remove_stopwords=True):
    words = []
    gram_info = []
    text = re.sub("[^а-яА-Я]"," ", text)
    all_words = text.lower().split()
    for word in all_words:
        p = morph.parse(word)[0]
        if word not in stop_words and  p.normal_form not in stop_words:
            words.append({word:p.normal_form})
            gram_info.append({p.normal_form:str(p.tag)})
    return(words,gram_info)
    
def dict_to_sentences(text,tokenizer, remove_stopwords=True):
    raw_sentences = tokenizer.tokenize(text.strip())
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append(dict_to_wordlist(raw_sentence, \
              remove_stopwords))
    return sentences

def lemmas_in_def(lemmas,sentences):
    c = 0
    lemma_counter = []
    for lemma in lemmas:
        for sentence in sentences:
            m = re.search(lemma,str(sentence))
            if m != None:
                c += 1
        lemma_count = {lemma:c}
        lemma_counter.append(lemma_count)
        c = 0  
    return(lemma_counter)
 
sentences = []
lemmas = []
normalized_forms = []
normalized_gram = []
nouns = []
i = 0
_dict = pd.read_csv( "C:\\Users\\Ania\\Desktop\\kursach\\1.csv", header=0, 
 delimiter=";")
for art in _dict["DEF"]:
    art = _dict["VOCAB"][i]+ ' ' + str(art)
    try:
        sentences += dict_to_sentences(str(art), tokenizer)
    except KeyError:
        continue 
    i += 1      

for sentence in sentences:
    for s in sentence:
        try:
            if len(s) == 0:
                sentences.remove(sentence)
        except ValueError:
            continue
    normalized_gram.append(sentence[-1])
    for word in sentence[-1]:
        word = str_key(word)        
        normalized_forms.append(word)
        if word not in lemmas:
            lemmas.append(word)
for forms in normalized_gram:
    for word in forms:
        line = str_value(word)
        m = re.search('NOUN',line)
        if m != None:
            nouns.append(str_key(word))
            
c = Counter(nouns).most_common()
#for element in c[:500]:
 #   if [element[0]] not in stop_words: 
  #      stop_words.extend([element[0]])

#lemma_counter = lemmas_in_def(lemmas,sentences)     
dice_dict = []
k_words = ["абажур"]
k_def = ''
for sentence in sentences:
    i = 0
    for word in k_words:
        under = len(sentence[0])
        for s in sentence:
            if str_key(s[0]) == word:
                k_def = sentence[0]
                for element in k_def:
                    for d in s:
                        if str_value(element) == str_key(d) and str_key(d) not in stop_words:
                            i += 1
            above = i
            dice = {(word,str_key(s[0])):above/under}
            if dice not in dice_dict:
                dice_dict.append(dice)

f = open('яблоко.txt','w',encoding = 'utf-8')
for dice in dice_dict:
    if str_value(dice) != '0.0':
        f.write(str(dice)+'\n')
f.close()



#f = open('frequency.csv','w',encoding = 'utf-8')
#for line in c:
#    f.write(line[0]+'\t'+str(line[1])+'\n')
#f.close()
#f = open('lemma_counter.csv','w',encoding = 'utf-8')
#for line in lemma_counter:
#    f.write(str(line)+'\n')
#f.close()