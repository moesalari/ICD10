# Capture ICD-10
# This program captures ICD-10 codes based on the input from users
# ICD-10.CSV file will be saved
# Source website is https://www.icd10data.com/



from lxml import html
import requests
import pandas as pd


# This function asks user for key words and return an array
def getwordKeys():
    userInput = ''
    wordsArray = []
    while userInput != 'end':
        userInput = input("Enter Key word: ")
        wordsArray.append(userInput)
    return wordsArray[:-1]



# This function returns url link based on the user key words  
def urlMaker(wordsArray):
    lenArray = len(wordsArray)
    if lenArray == 1:
        return 'https://www.icd10data.com/search?s='+wordsArray[0]
    else:
        urlstring = ''
        for i in range(1,lenArray):
            urlstring = urlstring+'%20'+wordsArray[i];
        urlstring = 'https://www.icd10data.com/search?s='+wordsArray[0]+urlstring;
    return urlstring
    
# this function capture icd10 codes from url 
def fetchICD10 (urlString):
    page = requests.get(urlString)
    tree = html.fromstring(page.content)
    icd10 = tree.xpath('//span[@class="identifier"]/text()')
    return(icd10)

def main():
    wordsArray = getwordKeys()
    urlString = urlMaker(wordsArray)
    print('\nGenerating url.... \nurl: '+ urlString)    
    icd10 = fetchICD10(urlString)
    for i in range(2,21):
        urlStringPage = urlString
        urlStringPage = urlStringPage + '&page=' + str(i)
        request = requests.get(urlStringPage)
        print('\nChecking all pages of https://www.icd10data.com/' )
        print('Page No'+str(i))
        if request.status_code == 200:
            icd10.extend(fetchICD10(urlStringPage))
    return icd10
print('\n\n########################Program Description########################')
print('This program captures ICD-10 codes based on the input from users. \nICD-10.CSV file will be saved at the end.\nSource website is https://www.icd10data.com/ .')
print('###################################################################')
print('\n')
print('Please enter key word one by one and press Enter\nTo end type "end" and press Enter')

icd10 = main() 
df = pd.DataFrame(icd10)
df = df.drop_duplicates()
df.to_csv(r'ICD10.csv')
print('\nICD10.csv has been saved')


 