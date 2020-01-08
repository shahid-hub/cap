#!/usr/bin/env python
# coding: utf-8

# # IBM Applied Data Science Capstone Course by Coursera
# ### Week 3 Part 1
# - Build a dataframe of the postal code of each neighborhood along with the borough name and neighborhood name in Toronto.
# ***
# ### 1. Import libraries

# In[1]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

import json # library to handle JSON files

from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML and XML documents

from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

import folium # map rendering library

print("Libraries imported.")


# ### 2. Scrap data from Wikipedia page into a DataFrame

# In[2]:


# send the GET request
data = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text


# In[3]:


# parse data from the html into a beautifulsoup object
soup = BeautifulSoup(data, 'html.parser')


# In[4]:


# create three lists to store table data
postalCodeList = []
boroughList = []
neighborhoodList = []


# **Using BeautifulSoup**
# 
# ```python
# # find the table
# soup.find('table').find_all('tr')
# 
# # find all the rows of the table
# soup.find('table').find_all('tr')
# 
# # for each row of the table, find all the table data
# for row in soup.find('table').find_all('tr'):
#     cells = row.find_all('td')
# ```

# In[5]:


# append the data into the respective lists
for row in soup.find('table').find_all('tr'):
    cells = row.find_all('td')
    if(len(cells) > 0):
        postalCodeList.append(cells[0].text)
        boroughList.append(cells[1].text)
        neighborhoodList.append(cells[2].text.rstrip('\n')) # avoid new lines in neighborhood cell


# In[6]:


# create a new DataFrame from the three lists
toronto_df = pd.DataFrame({"PostalCode": postalCodeList,
                           "Borough": boroughList,
                           "Neighborhood": neighborhoodList})

toronto_df.head()


# ### 3. Drop cells with a borough that is "Not assigned"

# In[7]:


# drop cells with a borough that is Not assigned
toronto_df_dropna = toronto_df[toronto_df.Borough != "Not assigned"].reset_index(drop=True)
toronto_df_dropna.head()


# ### 4. Group neighborhoods in the same borough
# 

# In[8]:


# group neighborhoods in the same borough
toronto_df_grouped = toronto_df_dropna.groupby(["PostalCode", "Borough"], as_index=False).agg(lambda x: ", ".join(x))
toronto_df_grouped.head()


# ### 5. For Neighborhood="Not assigned", make the value the same as Borough

# In[9]:


# for Neighborhood="Not assigned", make the value the same as Borough
for index, row in toronto_df_grouped.iterrows():
    if row["Neighborhood"] == "Not assigned":
        row["Neighborhood"] = row["Borough"]
        
toronto_df_grouped.head()


# ### 6. Check whether it is the same as required by the question

# In[10]:


# create a new test dataframe
column_names = ["PostalCode", "Borough", "Neighborhood"]
test_df = pd.DataFrame(columns=column_names)

test_list = ["M5G", "M2H", "M4B", "M1J", "M4G", "M4M", "M1R", "M9V", "M9L", "M5V", "M1B", "M5A"]

for postcode in test_list:
    test_df = test_df.append(toronto_df_grouped[toronto_df_grouped["PostalCode"]==postcode], ignore_index=True)
    
test_df


# ### 7. Finally, print the number of rows of the cleaned dataframe

# In[11]:


# print the number of rows of the cleaned dataframe
toronto_df_grouped.shape

