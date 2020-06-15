#!/usr/bin/env python
# coding: utf-8

# # Captstone Project for submission

# In[122]:


import requests
import lxml.html as lh
import pandas as pd
import numpy as np


# Scrapping Data

# In[94]:


url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'

#Create a handle, page, to handle the contents of the website
page = requests.get(url)

#Store the contents of the website under doc
doc = lh.fromstring(page.content)

#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')


# In[95]:


#Check the length of the first 12 rows
[len(T) for T in tr_elements[:12]]


# In[96]:


# Parse the first row as our header
tr_elements = doc.xpath('//tr')

#Create empty list
col=[]
i=0

#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print ('%d:"%s"'%(i,name))
    col.append((name,[]))


# In[97]:


#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 3, the //tr data is not from our table 
    if len(T)!=3:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1


# In[98]:


# Check the length of each column. Ideally, they should all be the same
[len(C) for (title,C) in col]


# The dataframe will consist of three columns: PostalCode, Borough, and Neighborhood

# In[99]:


Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)


# In[100]:


# Access the top 5 rows of the data frame 
df.head()


# In[101]:


df = df.replace('\n',' ', regex=True)
df.head()


# In[102]:


df.rename(columns={'Postal Code\n': 'Postal Code', 'Borough\n': 'Borough','Neighborhood\n':'Neighborhood'}, inplace=True)


# Only process the cells that have an assigned borough. Ignore cells with a borough that is Not assigned.

# In[114]:


df.drop(df.index[df['Borough'] == 'Not assigned '], inplace = True)

# Reset the index and dropping the previous index
df = df.reset_index(drop=True)

df.head(10)


# More than one neighborhood can exist in one postal code area. For example, in the table on the Wikipedia page, you will notice that M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park. These two rows will be combined into one row with the neighborhoods separated with a comma as shown in row 11 in the above table.

# In[117]:


df = df.groupby(['Postal Code', 'Borough'])['Neighborhood'].apply(','.join).reset_index()
df.columns = ['Postal Code','Borough','Neighborhood']
df.head(10)


# In[118]:


df['Neighborhood'] = df['Neighborhood'].str.strip()


# If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough.

# In[119]:


df.loc[df['Neighborhood'] == 'Not assigned ', 'Neighborhood'] = df['Borough']


# In the last cell of your notebook, use the .shape method to print the number of rows of your dataframe.

# In[120]:


df.shape


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




