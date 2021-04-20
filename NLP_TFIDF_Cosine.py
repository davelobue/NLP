
###########################################################################
#    Step 1:  Initial directory setup and file processing procedures
###########################################################################

#Relevant Packages import
import scrapy
import os

#Create JSON file for data storage
#Delete any prior .jl lines instead of appending:
if os.path.exists('texts.jl'):
    os.remove('texts.jl')
else:
    print("File does not yet exist, generating new output file")

# make directory for storing html documents sourced from web page
directory_name = 'philosophy'
if not os.path.exists(directory_name):
	os.makedirs(directory_name)

# function for iterating through and printing directory structure
def list_all(current_directory):
    for root, dirs, files in os.walk(current_directory):
        level = root.replace(current_directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

# examine the directory structure
# list the avaliable spiders
current_directory = os.getcwd()
list_all(current_directory)
print('\nScrapy spider names:\n')
os.system('scrapy list')


#Run Scrapy spider from these lines to extract text
# JSON format text outputs
os.system('scrapy crawl philosophy-spider -o texts.jl')
print('\nJSON lines written to texts.jl\n')


###########################################################################
#    Step 2:  Data Extraction and processing using BeautifulSoup
###########################################################################

# Process text data since original web pages scraped have a wide range of topics covered
# Start by breaking apart documents into sub sections, since overall articles can vary widely in topics:
# This will allow individual document retreival to be more focused

#Relevant Packages import
from collections import Counter
from bs4 import BeautifulSoup
import string
import re


#output path for cleaned individual text sections (language corpus)
page_dirname = 'corpus'
if not os.path.exists(page_dirname):
    os.makedirs(page_dirname)

#Below are a set of functions for processing HTML data 
#These are linked to extract relevant text for language processing

def process_htmldocs(directory):
    for filename in os.listdir(directory):
        path=directory + '/' + filename
        load_htmldoc(path)

def load_htmldoc(filename):
    file=open(filename, 'r')
    content=file.read()
    file.close()
    webtext=BeautifulSoup(content, 'html.parser')
    pagetext=webtext.find(id="main-text")
    #Identify sub headers for topic sections
    subject=[headers.text.encode('utf-8').decode('ascii', 'ignore') for headers in webtext.find_all('h1')]
    topics=[]
    for headers in pagetext.find_all('h2'):
        headers=headers.text.encode('utf-8').decode('ascii', 'ignore')
        removal=string.punctuation
        for item in removal:
            headers=headers.replace(item, '')
        topics.append(subject[0]+'_'+headers)

    #Split HTML sections by header classes
    fullbody=str(pagetext)
    body_split = re.split('(<h2>|</h2>)', fullbody)
    collection=[]
    for section in body_split:
        clean=BeautifulSoup(section, 'html.parser')
        paragraphs=clean.select('p')
        if paragraphs:
            collection.append(paragraphs)

    #split and clean each section of text
    counter=0
    for section in collection:
        text=''
        htmlstrip=['\n','<p>','</p>','<em>','</em>']
        for x in range(len(section)):
            sent=str(section[x].text)
            for item in htmlstrip:
                sent=sent.strip().replace(item, ' ')
            text=text +' '+ sent
        filename = page_dirname + '/' + topics[counter]+'.txt'
        save_list(text, filename)
        counter=counter+1

def save_list(lines, filename):
    file=open(filename, 'w')
    file.write(lines)
    file.close()

#Run above functions
process_htmldocs(page_dirname)


###########################################################################
#    Step 3:  Tokenize vocabulary & create list of frequently used words
###########################################################################

#import support functions written in dataprocesses.py file
import dataprocesses as dp

#Start by creating a vocabulary to pull from
def add_doc_to_vocab(filename, vocab):
    doc=dp.load_doc(filename)
    tokens=dp.clean_doc(doc)
    vocab.update(tokens)

def process_txtdocs(directory, vocab):
    for filename in os.listdir(directory):
        path=directory + '/' + filename
        add_doc_to_vocab(path, vocab)

def save_voc_list(lines, filename):
    data='\n'.join(lines)
    file=open(filename, 'w')
    file.write(data)
    file.close()

#Use Python counter function to assess vocab/term frequency
vocab=Counter()
process_txtdocs('corpus', vocab)
print('length of vocabulary:', len(vocab))

#set minimum word usage for qualifiaction to 3x
min_occurrence=3
tokens=[k for k,c in vocab.items() if c>min_occurrence]
print('number of tokens: ', len(tokens))

save_voc_list(tokens, 'vocab.txt')


###########################################################################
#    Step 4:  Process text data: create bag of words (clean & filter vocab)
###########################################################################

def doc_to_line(filename, vocab):
    doc=dp.load_doc(filename)
    tokens=dp.clean_doc(doc)
    tokens=[w for w in tokens if w in vocab]
    return ' '.join(tokens)

def process_docs(directory, vocab):
    lines=list()
    titles=list()
    for filename in os.listdir(directory):
        path=directory + '/' + filename
        line=doc_to_line(path, vocab)
        lines.append(line)
        titles.append(filename)
    return lines, titles

def load_clean_dataset(vocab):
    docs,labels=process_docs('corpus', vocab)
    return docs, labels

vocab_filename='vocab.txt'
vocab=dp.load_doc(vocab_filename)
vocab=set(vocab.split())
docs, labels=load_clean_dataset(vocab)

print('total number of documents: ', len(docs))
print('\n'*2)



###########################################################################
#    Step 5:  Create document classification scoring with TF-IDF algorithm
#    Step 6:  Retrieve relevant documents using cosine similarity algorithm
###########################################################################

#See dataprocess.py doc for functions

#Run from linux terminal, automated prompt asks user for a search query
#Enter query from terminal:

begin=input("Would you like to search the Stanford philosophy of languge corpus? (y/n)")
if begin=='y':
    dp.QA(docs, labels)
    ask_again=input("Would you like to search again? (y/n)")
    if ask_again=='y':
        dp.QA(docs, labels)
    else:
        pass
else:
    pass
