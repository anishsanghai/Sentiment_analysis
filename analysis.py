#importing the packages
import nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer,WordNetLemmatizer
import re
import pandas as pd

#making the stop words list for the analysis
with open(r'C:\Users\sangh\OneDrive\Desktop\Answers\StopWords\StopWords_Auditor.txt','r',encoding='latin-1') as f1,open(r'C:\Users\sangh\OneDrive\Desktop\Answers\StopWords\StopWords_Currencies.txt','r',encoding='latin-1') as f2,open(r'C:\Users\sangh\OneDrive\Desktop\Answers\StopWords\StopWords_DatesandNumbers.txt','r',encoding='latin-1') as f3,open(r'C:\Users\sangh\OneDrive\Desktop\Answers\StopWords\StopWords_Generic.txt','r',encoding='latin-1') as f4,open(r'C:\Users\sangh\OneDrive\Desktop\Answers\StopWords\StopWords_GenericLong.txt','r',encoding='latin-1') as f5,open(r'C:\Users\sangh\OneDrive\Desktop\Answers\StopWords\StopWords_Geographic.txt','r',encoding='latin-1') as f6,open(r'C:\Users\sangh\OneDrive\Desktop\Answers\StopWords\StopWords_Names.txt','r',encoding='latin-1') as f7:
  l=[f1,f2,f3,f4,f5,f6,f7]
  dem=''
  for i in l:
    dem+=' '.join(list(map(lambda a:a.lower(),list(map(lambda c:c[:-1] if ord(c[-1:]) ==10 else c[:],list(map(lambda b:b[0],list(map(lambda a:a.split(' '),i.readlines())))))))))
    i.close()
stopwords=dem.split(' ')
# making the master dictionary list for the analysis
file1=open(r'C:\Users\sangh\OneDrive\Desktop\Answers\MasterDictionary\negative-words.txt','r',encoding='latin-1')
file2=open(r'C:\Users\sangh\OneDrive\Desktop\Answers\MasterDictionary\positive-words.txt','r',encoding='latin-1')
pos=list(map(lambda a:a.lower(),list(map(lambda c:c[:-1] if ord(c[-1:]) ==10 else c[:],list(map(lambda b:b[0],list(map(lambda a:a.split(' '),file2.readlines()))))))))
neg=list(map(lambda a:a.lower(),list(map(lambda c:c[:-1] if ord(c[-1:]) ==10 else c[:],list(map(lambda b:b[0],list(map(lambda a:a.split(' '),file1.readlines()))))))))
file1.close()
file2.close()
output=pd.read_excel('Output_Data_Structure.xlsx')
#function for pre_processing the text
def pre_processing(dat):
  dat=' '.join(dat)
  # converting the given text to lower text
  dat=dat.lower()
  # removing all the urls from the text
  dat=re.sub(r'^https?:\/\/.*[\r\n]*', '', dat, flags=re.MULTILINE)
  # removing the special characters from the text
  dat=re.sub('[^A-Za-z0-9]+', ' ', dat)
  # removing the punctuations from the text
  dat=re.sub(r'[^\w\s]','',dat)
  # tokenizing the data
  bro=word_tokenize(dat)
  # getting rid of the stopwords as well as the unnecessary spaces that comes in the list
  filter_words=' '.join(list(map(lambda a :a if a not in stopwords else '',bro))).split()
  # Stemming the words
  ps=PorterStemmer()
  stemmed_words=[ps.stem(w) for w in filter_words]
  #lematizing the words
  lematizer=WordNetLemmatizer()
  lemma_words=[lematizer.lemmatize(w,pos='a') for w in stemmed_words]
  return lemma_words
#function for analysis
def analysis(data,raw_data):
  #function for counting the number of syllables
  def count_syllables(word):
    return len(
        re.findall('(?!e$)[aeiouy]+', word, re.I) +
        re.findall('^[^aeiouy]*e$', word, re.I)
    )  
  res={}
  p,n=0,0
  #calculating the positive and negative score
  for i in data:
    if i in pos:
      p+=1
    elif i in neg:
      n+=1
  res['POSITIVE SCORE']=p
  res['NEGATIVE SCORE']=n
  res['POLARITY SCORE']=(p-n)/(p+n+0.000001)
  res['SUBJECTIVITY SCORE']=(p+n)/(len(data)+0.000001)
  raw_data=' '.join(list(map(lambda a :a[:-1]if ord(a[-1:])==10 else a[:],raw_data))).replace(u'\xa0', u' ').split('.')
  res['AVG SENTENCE LENGTH']=len(data)/len(raw_data)
  num_complex_words=list(map(lambda a: 1 if count_syllables(a)>2 else 0,data)).count(1)
  res['PERCENTAGE OF COMPLEX WORDS']=num_complex_words/len(data)
  res['FOG INDEX']=0.4*(res['PERCENTAGE OF COMPLEX WORDS']+res['AVG SENTENCE LENGTH'])
  res['AVG NUMBER OF WORDS PER SENTENCE']=res['AVG SENTENCE LENGTH']
  res['COMPLEX WORD COUNT']=num_complex_words
  res['WORD COUNT']=len(data)
  res['SYLLABLE PER WORD']=sum(list(map(lambda a: count_syllables(a),data)))
  pronounRegex = re.compile(r'\bI\b|\bwe\b|\bWe\b|\bmy\b|\bMy\b|\bus\b|\bhe\b|\bHe\b|\bme\b|\byou\b|\bit\b|\bIt\b|\bshe\b|\bShe\b|\bhim\b|\bher\b|\bthey\b|\bThey\b|\bthem\b|')
  raw_data=' '.join(raw_data)
  res['PERSONAL PRONOUNS']=len(' '.join(pronounRegex.findall(raw_data)).split())
  res['AVG WORD LENGTH']=sum(list(map(lambda a: len(a),data)))/len(data)
  return res
#iterating through the files
for i in range(37,150):
  raw_data=[]
  path='extracted_files/'+str(i)+'.txt'
  try:
    file=open(path,'r',encoding='utf-8')
    raw_data=file.readlines()
    file.close()
  except:
    raw_data=None
  res={}
  if raw_data:
    res=analysis(pre_processing(raw_data),raw_data)
  else:
    res={
      'POSITIVE SCORE':'website not found',
      'NEGATIVE SCORE':'website not found',
      'POLARITY SCORE':'website not found',
      'SUBJECTIVITY SCORE':'website not found',
      'AVG SENTENCE LENGTH':'website not found',
      'PERCENTAGE OF COMPLEX WORDS':'website not found',
      'FOG INDEX':'website not found',
      'AVG NUMBER OF WORDS PER SENTENCE':'website not found',
      'COMPLEX WORD COUNT':'website not found',
      'WORD COUNT':'website not found',
      'SYLLABLE PER WORD':'website not found',
      'PERSONAL PRONOUNS':'website not found',
      'AVG WORD LENGTH':'website not found'}
# writing the output to the given excel sheet 
  for j in res:
    output[j][i-36]=res[j]
output.to_excel('output.xlsx')

  

