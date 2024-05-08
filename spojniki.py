#!/usr/bin/env python
# coding: utf-8

from __future__ import division
import pandas as pd
__author__ = 'Agnieszka'
__project__ = 'spojniki'
import re, nltk, pprint
from operator import itemgetter


#korpus

corpus = open("all_raw.txt", 'r', encoding= "utf8").read()


#podział korpusu na zdania i zdań na wyrazy (tokenizacja)

nltk.download('punkt')

sent_tokenizer = nltk.data.load("tokenizers/punkt/polish.pickle")

def words_in_sents(list):
    new = []
    for s in list:
        s = s.lower()
        new.append(nltk.word_tokenize(s))
    return new

words = nltk.word_tokenize(corpus)

sentences = sent_tokenizer.tokenize(corpus)

words_sentences = words_in_sents(sentences)

#liczba zdań i wyrazów w korpusie
len(words_sentences)
len(words)


#lista spójników

connectors = ["a", "aby", "acz", "aczkolwiek", "albo", "albowiem", "ale", "alias", "ani", "aniżeli", "aż", "ażeby", "bądź", 
            "bo", "boby", "bowiem", "by", "byle", "byś", "choć", "choćby", "chociaż", "chyba że", "czy", "czyli", "dlatego", 
            "dopóki", "dopóty", "dotąd", "gdy", "gdyby", "gdyż", "i", "i tak", "ilekroć", "iż", "jak", "jakby", "jakkolwiek", 
            "jako że", "jednak", "jednakże", "jeśli", "jeżeli", "kiedy", "lecz", "ledwie", "ledwo", "lub", "mianowicie", 
            "mimo to", "natomiast", "niby", "niczym", "niż", "oprócz tego", "oraz", "po czym", "podczas gdy", "póki", "ponieważ", 
            "póty", "poza tym", "skoro", "toteż", "więc", "wprawdzie", "zamiast", "zanim", "zarówno", "zaś", "zatem", "że", "żeby"]


#funkcje do wyszukiwania wystąpień spójników i rdzenia "któr-"

def findWholeWord(w, text):
    return re.findall(r'\b({0})\b'.format(w), text, flags=re.IGNORECASE)

def find_word_starting_with(w, text):
    return re.findall(r'\b({0})'.format(w), text, flags=re.IGNORECASE)

def find_connectors(words, text):
    new_list = []
    for s in words:
        new_list.append(findWholeWord(s, text))
    new_list.append(find_word_starting_with('któr', text))
    return new_list

all_connectors = find_connectors(connectors, corpus)


#zliczanie wystąpień poszczególnych spójników i zaimka względnego

def count_connectors(list):
    withnumbers = []
    for s in list:
        if len(s) > 0:
            withnumbers.append((s[0], len(s)))
    return sorted(withnumbers, key=itemgetter(1))


count_connectors(all_connectors)


# najczęściej występujące wyrazy wprowadzające zdania podrzędne

subordinators=['czy', 'gdy', 'kiedy', 'że', 'aby', 'żeby', 'by', 'byś', 'jeśli', 'jeżeli', 'gdyby', 'któr']


# wyszukiwanie zdań złożonych podrzędnie

def findsentences(sents_tokenized, sents, conn):
    found = []
    for s in sents_tokenized:
        for k in conn:
            if k in s:
                if sents[sents_tokenized.index(s)] not in found:
                    found.append(sents[sents_tokenized.index(s)])
    return found

withconnectors = findsentences(words_sentences, sentences, subordinators)

len(withconnectors)


# filtrowanie zdań z "czy" - usunięcie zdań pytających

def czysubordinate(sent_tokenized, sent):
    selection =  []
    for s in sent_tokenized:
        if "czy" in s and s[0] != "czy":
            selection.append(sent[sent_tokenized.index(s)])
    return selection


def czynotsubordinate(sent_tokenized, sent):
    neg_selection = []
    for s in sent_tokenized:
        if s[0] == "czy":
            neg_selection.append(sent[sent_tokenized.index(s)])
    return neg_selection

subczy=czysubordinate(words_sentences, sentences)

len(subczy)

notsub = czynotsubordinate(words_sentences, sentences)

len(notsub)




-----

jesli = "jeśli"

def findktor(listoflists):
    ktor = []
    for s in listoflists:
        for x in s:
            if x.startswith('któr'):
                ktor.append(x)
    return ktor


# In[23]:


ktor = findktor(words_sentences)


# In[24]:


def clean(list):
    new = []
    for k in list:
        if k not in new:
            new.append(k)
    return new


# In[60]:


print(ktor)


# In[25]:


ktor_czysty=clean(ktor)


# In[26]:


ktor_czysty


# In[30]:


losowezdanie1(words_sentences, ["którą", "którego", "których"])


# In[31]:


losowezdanie1(words_sentences, ktor)


# In[ ]:





# In[32]:


losowezdanie1(words_sentences, ["kiedy", "gdy"])


# In[33]:


losowezdanie(words_sentences, "że")


# In[34]:


losowezdanie1(words_sentences, ["by", "aby", "żeby"])


# In[27]:


ilektorow = len(ktor)


# In[28]:


print(ilektorow)


# In[29]:


def przypadek(zbior, formy):
    lista_form = []
    for w in zbior:
        if w in formy:
            lista_form.append(w)
    return lista_form


# In[30]:


ktormianownik = przypadek(ktor, ['który', 'która', 'które', 'którzy'])


# In[31]:


len(ktormianownik)


# In[32]:


ktorbiernik = przypadek(ktor, ['którą', 'którego', 'których'])


# In[33]:


len(ktorbiernik)


# In[34]:


ktornarzednik = przypadek(ktor, ['którymi', 'którym'])


# In[35]:


len(ktornarzednik)


# In[36]:


ktory_lista = pd.read_csv("ktory_przypadki_naczysto.csv", sep = ";", index_col=None, engine = "python", encoding = 'UTF8')


# In[45]:


def ktordrucker(lista, sents, table, formy):
    for s in lista:
        for k in formy:
            if k in s:
                if k in ['która', 'którzy']:
                    table.loc[len(table)+1] = (sents[lista.index(s)], k, 'M')
                elif k == 'któremu':
                    table.loc[len(table)+1] = (sents[lista.index(s)], k, 'C')
                elif k == 'którymi':
                    table.loc[len(table)+1] = (sents[lista.index(s)], k, 'N')
                else:
                    table.loc[len(table)+1] = (sents[lista.index(s)], k, '')
    return table


# In[ ]:





# In[46]:


ktorprzypadki = ktordrucker(words_sentences, sentences, ktory_lista, ktor_czysty)


# In[ ]:





# In[ ]:


ktorprzypadki=ktorprzypadki.sort("przypadek")


# In[131]:


ktorprzypadki


# In[118]:


'''def ktor_nmian(listoflists, table, listazdan):
    for s in listoflists:
        for x in s:
            if x.startswith('któr'):
                if x not in ['która', 'którzy']:
                    table.loc[len(table)+1] = (x, listazdan[listoflists.index(s)])
    return table'''


# In[132]:


'''ktory_lista = ktor_nmian(words_sentences, ktory_lista, sentences)'''


# In[133]:


ktory_lista


# In[47]:


ktory_lista.to_csv("ktory_przypadki.csv", encoding="utf-8")
ktory_lista.to_excel("ktory_przypadki.xlsx", encoding="utf-8")


# In[135]:


ktorprzypadki.to_csv("ktory_przypadki_naczysto.csv", encoding="utf-8")
ktorprzypadki.to_excel("ktory_przypadki_naczysto.xlsx", encoding="utf-8")


# In[138]:


ktory_niemian = pd.read_excel("ktory_przypadki.xlsx")


# In[140]:


ktory_complete=pd.read_excel("ktory_przypadki_naczysto1.xlsx")


# In[141]:


ktory_complete


# In[142]:


przyp = ktory_complete["przypadek"].unique()


# In[143]:


przyp


# In[147]:


przyp_zliczone = pd.DataFrame({"Liczba": [len(ktory_complete[ktory_complete["przypadek"] == k]) for k in przyp]}, index = [k for k in przyp]).sort()
przyp_zliczone.sort("Liczba")


# In[ ]:





# In[61]:


def jeslito(sent_tokenized, sent):
    zdaniazto = []
    for s in sent_tokenized:
        for k in ["jeśli", "jeżeli"]:
            if k in s:
                if "to" in s:
                    zdaniazto.append(sent[sent_tokenized.index(s)])
    return zdaniazto
                


# In[62]:


len(jeslito(words_sentences, sentences))


# In[63]:


jeslito(words_sentences, sentences)


# In[64]:


ktory_lista.to_csv("ktory_przypadki_wszystkie.csv", encoding="utf-8")
ktory_lista.to_excel("ktory_przypadki_wszystkie.xlsx", encoding="utf-8")


# In[40]:


def ktor_mian_bankowo(sent_tokenized, sent):
    zbior = []
    for s in sent_tokenized:
        for k in ["która", "którzy"]:
            if k in s:
                zbior.append(sent[sent_tokenized.index(s)])
    return zbior                


# In[41]:


len(ktor_mian_bankowo(words_sentences, sentences))


# In[42]:


ktor_mian_bankowo(words_sentences, sentences)


# In[73]:


162+59



def dopcokto(sent, sent_tokenized, cokto):
    lista =  []
    for s in sent_tokenized:
        for w in cokto:
            if w in s and s.index(w) != 0:
                lista.append(sent[sent_tokenized.index(s)])
    return lista


# In[95]:


cokto = ['co', 'czego', 'czemu', 'czym', 'kto', 'kogo', 'komu', 'kim']


# In[96]:


cokto1 = dopcokto(sentences, words_sentences, cokto)


# In[97]:


len(cokto1)


# In[98]:


cokto1


# In[33]:


findsentences(words_sentences, sentences, ['kiedy'])


# In[35]:


findsentences(words_sentences, sentences, ['co', 'czego', 'czemu', 'czym', 'kto', 'kogo', 'komu', 'kim', 'gdzie', 'jak'])


# In[37]:


def findparticiple(sents, sents_tokenized, endings):
    zimieslowami=[]
    for s in tokenized:
        for x in s:
            for e in endings:
                if x.endswith(e):
                    zimieslowami.append(sents[tokenized.index(s)])
    return zimieslowami


# In[38]:


koncowki_imiesl=['ący', 'ącego', 'ącemu', 'ącego', 'ącym', 'ąca', 'ącej', 'ącą', 'ące', 'ących', 'ącymi']


# In[40]:


imieslowy=findparticiple(sentences, words_sentences, koncowki_imiesl)


# In[62]:


findsentences(words_sentences, sentences, ['jeśli', 'jeżeli'])


# In[56]:


def nibywarunkowe(sentences, str):
    wykaz=[]
    for s in sentences:
        if str in s:
            wykaz.append(s)
    return wykaz


# In[57]:


nibywarunkowe(sentences, 'jeśli chcesz')


# In[61]:


dopelnieniowe=findsentences(words_sentences, sentences, ['że'])


# In[63]:


def filter(sentences, lista):
    wykaz = []
    for s in sentences:
        for w in lista:
            if w in s:
                wykaz.append(s)
    return wykaz


# In[66]:


len(filter(dopelnieniowe, ['znaczy', 'oznacza', 'polega', 'mówimy', 'mówi']))


# In[73]:


spojniki1=["azali", "boć", "byleby", "chociażby", "chybaby", "co", "cokolwiek", "czyj", "dlaczego",
           "dokąd", "dokądkolwiek", "dopiero", "gdzie", "gdziekolwiek", "ile", "ilekolwiek", "ilekroć", 
           "iżby", "jaki", "jakikolwiek", "jako", "jakżeby", "jeżeliby", "jeśliby", "kędy", "kiedykolwiek", 
           "kiedyż", "kim", "kogo", "komu", "kto", "ktokolwiek", "którędy", "mimo", "niech", "odkąd", 
           "pomimo", "skąd", "skądkolwiek", "zaledwie", "zwłaszcza", "czyja", "czyje", "czyjego", "czyjej", "czyjemu", "czyją", "czyim", "czyi", "czyich", "czyim", "czyimi"]


# In[74]:


uzup=wszystkie = find_connectors(spojniki1, korpus)


# In[75]:


count_connectors(uzup)


# In[71]:


def findkolwiek(listoflists):
    kolwieki = []
    for s in listoflists:
        for x in s:
            if x.endswith('kolwiek'):
                kolwieki.append(x)
    return kolwieki


# In[72]:


findkolwiek(words_sentences)


# In[99]:


dopelnieniowe_co=findsentences(words_sentences, sentences, cokto)


# In[101]:


len(dopelnieniowe_co)


# In[102]:


pytajne=["co", "czego", "czemu", "czym", "kto", "kogo", "komu", "kim", "gdzie", "ile", "dlaczego", "jaki", "skąd", "dokąd"]


# In[106]:


pytajnozalezne=findsentences(words_sentences, sentences, pytajne)


# In[107]:


len(pytajnozalezne)


# In[109]:


def nienapoczatku(sent_tokenized, sent, words):
    lista =  []
    for s in sent_tokenized:
        for w in words:
            if w in s and s[0] != w:
                lista.append(sent[sent_tokenized.index(s)])
    return lista


# In[111]:


len(nienapoczatku(words_sentences, sentences, pytajne))


# In[17]:


zeby=findsentences(words_sentences, sentences, ['żeby', 'aby', 'by'])


# In[18]:


zeby


# In[19]:


findsentences(words_sentences, sentences, ['byś'])


# narzędzia do wyświetlania losowego zdania z zadanymi wyrazami

import random

def randomsentence(sents, conn):
    selection = []
    for s in sents:
        if conn in s:
            selection.append(s)
    return random.choice(selection)

def randomsentence1(sents, options):
    selection = []
    for s in sents:
        for conn in options:
            if conn in s:
                selection.append(s)
    return random.choice(selection)

