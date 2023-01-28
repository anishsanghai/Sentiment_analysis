#importing the packages
import pandas as pd  
import requests
from bs4 import BeautifulSoup as bs 
#getting the data
data=pd.read_excel('Input.xlsx')
#going through the data frame and getting the articles
for i in range(0,114):
    r=requests.get(url=data['URL'][i],
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'})
    soup=bs(r.text,'html.parser')
    path='extracted_files/'+str(data['URL_ID'][i])+'.txt'
    #condition for checking if the website is present or not
    if soup.find('h1',class_='entry-title')==None:
        continue
    file=open(path,'w',encoding="utf-8")
    file.write(soup.find('h1',class_='entry-title').get_text()+'\n')
    #function for getting the content from the website and making it into a proper text document
    file.writelines('\n'.join(list(map(str,list(map(lambda a: a.get_text(),list((soup.find_all('p')))))))))
    file.close()
