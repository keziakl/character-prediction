# table scraper for http://hanzidb.org/character-list/general-standard?page=
# pages 1 - 82
# organizes character data into panda

import requests
import lxml.html as lh
import pandas as pd

# ACCESSING WEBSITE
# the Table of General Standard Chinese Characters contains 82 pages
# of characters. For the url for the next page, simply change
# the number following "page="
url_base = "http://hanzidb.org/character-list/general-standard?page="
# temporary value for to-be-returned panda structure
df = None

#BASIC SCRAPER FUNCTION
def scrapey(url):
    #grab first page
    page = requests.get(url)
    #store content of page in doc
    doc = lh.fromstring(page.content)
    #parse data stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')


    #STORING TABLEHEADER
    col = [] #2d array to be filled and converted to pd
    i = 0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        if i == 0:
            col.append(("Character", []))
        else:
            col.append((name,[]))

    #STORING NON-HEADER ROWS FROM TABLE
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T = tr_elements[j]
        #If row is not of size 8, the //tr data is not from our table
        if len(T) != 8:
            break
        #i is the index of our column
        i = 0
        #Iterate through each element of the row
        for t in T.iterchildren():
            #assigns data to specific box in table row=t, col=i
            data = t.text_content()
            col[i][1].append(data)
            #Increment i for the next column
            i += 1

    #CREATE AND RETURN PANDA STRUCTURE
    Dict = {title : column for (title, column) in col}
    df = pd.DataFrame(Dict)
    return df
    

#calling scrapey for all 82 webpages
for x in range(1, 83):
    df_temp = scrapey(url_base + str(x))
    #if first webpage of 82 to be appended
    try:
        df = df.append(df_temp, ignore_index = True)
    except:
        df = df_temp

print(df)
