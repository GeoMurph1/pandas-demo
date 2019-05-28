#!/usr/bin/env python
# coding: utf-8

# # Pandas DataFrame Demo - the basics
# ## by Michael J. Murphy, May 2019

# Let's create a simple pandas DataFrame from scratch:

# In[ ]:


import pandas as pd

df1 = pd.DataFrame({'A': [1, 2, 3, 4], 'B':[1, 4, 9, 16], 'C':[1, 8, 27, 64]})

print(df1)


# Slice a section of the DataFrame, using the index accessor, .iloc:

# In[ ]:


df1_sliced = df1.iloc[0:2, 1:]
print(df1_sliced)


# Now, let's create a DataFrame that's a bit more like what we see on a typical electronic data deliverable (EDD):

# In[ ]:


df2 = pd.DataFrame({'ID':['MW-1', 'MW-2', 'MW-3', 'SB-1', 'SB-2'],                     'Date': ['05/05/2019', '05/05/2019', '05/05/2019', '05/06/2019', '05/06/2019'],                    'Matrix': ['water', 'water', 'water', 'soil', 'soil'],                    'Units': ['ug/L', 'ug/L', 'ug/L', 'mg/kg', 'mg/kg'],                    'As': [0.555, 1.32, 0.710, 0.075, 0.17],                    'Be': [0.777, '<0.005', 0.910, 0.045, 0.088],                    'Cd': [0.333, 0.230, '<0.05', 0.056, 0.099]})
print(df2)


# Now, what if we only want records where water is the matrix? This is easily done using the .loc accessor:

# In[ ]:


df3 = df2.loc[df2['Matrix']== 'water']
print(df3)


# Alright, now we have the records we want. This format is great for a human-readable table, but it's not very useful if we want to import these records into a database. Let's melt this table down!

# In[ ]:


df4 = pd.melt(df3, id_vars = ['ID', 'Date', 'Matrix', 'Units'], value_vars = ['As', 'Be', 'Cd'],              var_name = 'Analyte', value_name = 'Result')
print(df4)


# Now, we have our data in a long-format table that can be imported into a database. What if we want to add a new column for the '<' prefixes for ND results? Easily done with our .loc tool!

# In[ ]:


df4['Prefix'] = ''
df4.loc[df4['Result'].str.contains('<') == True, 'Prefix'] = '<'
print(df4)


# Finally, let's do some housekeeping. We no longer need the '<' prefix in the result column, and the result values should be numbers (floats), not strings, for import to a database. 

# In[ ]:


import numpy as np

df4['Result_1'] = df4['Result']
df4['Result_1'] = df4['Result_1'].str.lstrip('<')
df4['Result_1'] = df4['Result_1'].fillna(df4['Result'])
df4['Result'] = pd.to_numeric(df4['Result_1'])
print(df4.Result)


# Additionally, the column order is kind of odd; let's rearrange it into a more logical order. 

# In[ ]:


df5 = df4[['ID', 'Date', 'Analyte', 'Prefix', 'Result', 'Matrix']]
print(df5)


# This short intro has illustrated some of the key tools and concepts of pandas DataFrames, and how they can be used in environmental data analysis. Next, let's take a look at a real-life example, using a historical dataset with over 40,000 records. 
