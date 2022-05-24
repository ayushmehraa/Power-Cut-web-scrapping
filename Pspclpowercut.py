from datetime import date
import requests
from bs4 import BeautifulSoup

url='https://distribution.pspcl.in/returns/module.php?to=Feeders.viewPlannedShutdownsPrintFormat'
req=requests.get(url)
content=req.text
# with open("PspclScrapy.html","w+")as file:
#     file.write(content)

soup=BeautifulSoup(content,"lxml")
columnsName=[]
table=soup.find("table",class_="aodb_table")


# col=table.find_all("th",class_="aodb_table_th")
# for data in col:
#     cols=data.text
#     columnsName.append(cols)

todayDate=date.today().strftime('%d/%m/%Y')

lastIndexOFSrNo=0
listOFRows=[]
rowsbody=soup.find("tbody")
allRows=rowsbody.find_all("tr")
for i,data in enumerate(allRows): 
    dataframe={}
    rowlength=len(data.text)

    rows=data.text
    # print(data.text)
    dataframe['Sr No']=rows[1:3].strip('\n')
    dataframe['Date']=rows[3:14].strip('\n')
    rowCitylength=len(data.text)-18 #18 is 17-1 string length of total time
    dataframe['Town/ City']=rows[14:rowCitylength-1].strip('\n')

    rowfromend=rowCitylength+8

    dataframe['From']=rows[rowCitylength:rowfromend].strip('\n')
    dataframe['To']=rows[rowfromend+1:rowlength-1].strip('\n')
    
    if (todayDate)==str(dataframe['Date']).strip():
        # print(f"{i+1}.{dataframe['Date']}") #for checking correct number of toady entries
        lastIndexOFSrNo=dataframe["Sr No"]
        listOFRows.append(dataframe)
    else:
        continue


    
# print(listOFRows)


import pandas as pd
['Sr No', 'Date', 'Town/ City', 'Area Affected', 'From', 'To']

#appending new data to pspcl.csv
# ------------------------------------uncomment below for appending new data/rows------------------------------------

df = pd.DataFrame(listOFRows)
df2=pd.to_excel("PSPCl.xls")
df2 = df2.append(df, ignore_index =False)
df2.to_excel(f'PSPCl.xls', index=False)
print(df2)



# ------------------------------------------------------------------------------------------------------------------#


# ---------------------uncomment below for creating a new file or overiding over current file---------------------

# ['Sr No', 'Date', 'Town/ City', 'Area Affected', 'From', 'To']
# df=pd.DataFrame(listOFRows)
# # df.to_csv(f'PSPCl.csv', index=False,)
# df.to_excel(f'PSPCl.xls', index=False,)


print('Done!!')