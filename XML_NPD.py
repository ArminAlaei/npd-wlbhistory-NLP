

#Importing the needed packages to parse and extract the relevant
#information from the XML files.

import pandas as pd
import numpy as np
import os
import sys
from xml.dom import minidom
import requests
from lxml import etree
from lxml.etree import fromstring
import urllib
import csv
import xml.etree.ElementTree as ET
from xml import *
import re
import xml.etree.cElementTree as EC
from bs4 import BeautifulSoup
import nltk
from pandas import *

#Parsing the XML file and getting the root
tree=ET.parse('wellbore_history.xml')
root=tree.getroot()

elemList = []



for elem in tree.iter():
    elemList.append(elem.tag)

elemList=list(set(elemList))

for c in root.findall('Detail_Collection'):
    well= c.get('Detail').text

wells=[]
for detail in root.iter('{wellbore_history}Detail'):
    wells.append(detail.attrib)

wellbore=[]
NPDID=[]
History=[]
for well in wells:
    wellbore.append(well['wlbName'])
    NPDID.append(well['wlbNPDID_wellbore'])
    History.append(well['wlbHistory'])

#Here we print the len of all the lists so we can be sure that
#the length of all three lists match.
print(len(wellbore))
print(len(NPDID))
print(len(History))

#In the part below we will turn each wellbore history/description
#into plain text in each row of the dataframe. The purpose of this is
#ofcourse to get rid of all HTML tags that may cause problems during our natural language processing.

newHist=[]
for text in History:
    soup = BeautifulSoup(text,features="lxml")      #lxml is the type of tags that hold our text.
    newText=soup.get_text()
    newHist.append(newText)
df1=pd.DataFrame(list(zip(wellbore,NPDID,newHist)),
    columns=['Wlb', 'ID', 'Hist'])
############################################################################################################################
############################################################################################################################
#NATURAL LANGUAGE PROCESSING
df3=df1.copy()
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

liste = []
for story in df3['Hist']:
    liste.append(story)
    sent_tokenize_list = sent_tokenize(story)
    wel = df3.loc[df3['Hist'] == story, ['Wlb']]
    wbid = df3.loc[df3['Hist'] == story, ['ID']]
    for sentence in sent_tokenize_list:
        if 'Surface pressure' in sentence:


            print('+++++++++++++++++++++++++++++++++++ Surface pressure +++++++++++++++++++++++++++++++++')
            print("WELLNAME: ", wel)
            print(sentence)
            # for tekst in sent_tokenize_list:
            #     soup = BeautifulSoup(tekst, features="lxml")  # lxml is the type of tags that hold our text.
            #     nTekst = soup.get_text()
            # print(nTekst)
        elif 'bottom hole pressure' in sentence:
            print('++++++++++++++++++++++++++++++++++++ bottom hole pressure +++++++++++++++++++++++++++++++++')
            print("WELLNAME: ", wel)
            print(sentence)
        elif 'reservoir pressure' in sentence:
            print('++++++++++++++++++++++++++++++++++++ reservoir pressure +++++++++++++++++++++++++++++++++')
            print("WELLNAME: ", wel)
            print(sentence)
        elif 'well head pressure' in sentence:
            print('+++++++++++++++++++++++++++++++++++++ well head pressure ++++++++++++++++++++++++++')
            print("WELLNAME: ", wel)
            print(sentence)

