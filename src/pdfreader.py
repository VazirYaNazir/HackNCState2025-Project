from pypdf import PdfReader
import sqlite3 as sql
import numpy as np

import requests
from nltk.tokenize import word_tokenize
from nltk.util import bigrams
import nltk
nltk.download('punkt_tab')

reader = PdfReader("pdfs/PrinciplesofFinance-WEB.pdf")
for page in reader.pages:
    print(page.extract_text())


def clean_string(str):
    # Keep only alphabetical characters in the string
    cleaned_string = ""
    for char in str:
        if char.isalpha() or char==" ":  # Check if the character is a letter or a space
            #line missing here!!!
            cleaned_string += char

    return cleaned_string.lower()

def word_count_dictionary(str1):
#returns a dictonary containing frequencies of any word in string
#e.g. str1 = 'quick brown fox is quick.'
    x = {}
    str1 = clean_string(str1)
    words = word_tokenize(str1)
    for b in words:
        if b in x:
            x[b]+=1
        else:
            x[b] = 1
    return(x)


def word_vector(word_set, word_dict):
    vector = []
    for word in word_set:
        # Get the value from word_dict or use 0 if the word is not found
        value = word_dict.get(word, 0)
        vector.append(value)
    return vector

def build_clean_set(*dicts):
    s = set() #makes empty set
    for d in dicts:
        for word in d.keys():
            s.add(word)
    return sorted(s)


def make_vectors(strings):
    word_dicts = []
    for s in strings:
        word_dicts.append(word_count_dictionary(s))
    word_set = build_clean_set(word_dicts)
    vectors = []
    for d in word_dicts:
        vectors.append(word_vector(word_set,d))
    print(word_set)
    return vectors

def angleBetweenVectors(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    dotProduct = np.dot(v1,v2)
    magnitudeMultiply = np.linalg.norm(v1) * np.linalg.norm(v2)
    angle_in_rad = np.arccos(dotProduct/magnitudeMultiply)
    angle_in_degrees = np.degrees(angle_in_rad)
    return angle_in_degrees


def createVectorsQuestionWithPdfs(question, pdfs):
    pdfTexts = []
    for pdf in pdfs:

        # creates a pdf string.
        pdfText = ""
        reader = PdfReader(pdf)
        for page in reader.pages:
            pdfText += page.extract_text() + " "

        pdfTexts.append(pdfText)

    pdfTexts.append(question)

    return make_vectors(pdfTexts)



