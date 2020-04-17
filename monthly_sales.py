import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime as dt
from itertools import combinations
from collections import Counter


#  Get All files from the directry and combine to create a single CSV

# files = [file for file in os.listdir('./Pandas-Data-Science-Tasks/SalesAnalysis/Sales_Data')]
# all_months_data = pd.DataFrame()

# for file in files:
# 	df = pd.read_csv('./Pandas-Data-Science-Tasks/SalesAnalysis/Sales_Data/'+file)
# 	all_months_data = pd.concat([all_months_data, df])

# all_months_data.to_csv("all_data.csv", index=False)

all_data = pd.read_csv('all_data.csv')
print(all_data.head())


# Clean Data
 drop na 

nan_df = all_data[all_data.isna().any(axis=1)] 
print(nan_df.head())
all_data = all_data.dropna(how='all')
print(all_data.head())

#  Add Month Column

all_data['Month'] = all_data['Order Date'].str[0:2]
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
all_data['Month'] = all_data['Month'].astype('int32')
# print(all_data.head())


# Convert quantity ordered and price each to int from str

all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])
print(type(all_data['Quantity Ordered'][0]), type(all_data['Price Each'][0]))


#  Add Sales Column

all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
print(all_data.head())


# Question: Which is the best for sales
results = all_data.groupby('Month').sum()

#  plot the graph

months = range(1, 13)
plt.bar(months, results['Sales'])
plt.xticks(months)
plt.xlabel('Month number.')
plt.ylabel('Sales in US $.')
plt.show()

# Add a city column
# use apply
def get_city(address):
	return address.split(',')[1]

def get_state(address):
	return address.split(',')[2].split(' ')[1] 


all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")
print(all_data.head())

# Question: What city has the highest number of display
r = all_data.groupby('City').sum()
print(r)

#  plot the graph

cities = [city for city, df in all_data.groupby('City')]
plt.bar(cities, r['Sales'])
plt.xticks(cities, rotation='vertical', size=8)
plt.xlabel('City Name.')
plt.ylabel('Sales in US $.')
plt.show()

#  get order date

all_data['Order date'] = pd.to_datetime(all_data['Order Date'])
all_data['Hour'] = all_data['Order date'].dt.hour
all_data['Minute'] = all_data['Order date'].dt.minute
print(all_data.head())


# Question: What time should we advertise to maximizelikelihood of customer buying a product
hours =  [hour for hour, df in all_data.groupby('Hour')]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hours')
plt.ylabel('No Of Orders')
plt.grid()
plt.show()


# Which products are most often sold together

# print(all_data.head(20))
duplicate_samples = all_data[all_data['Order ID'].duplicated(keep=False)]
duplicate_samples['Grouped'] = duplicate_samples.groupby('Order ID')['Product'].transform(lambda x:','.join(x))
duplicate_samples = duplicate_samples[['Order ID', 'Grouped']].drop_duplicates()
print(duplicate_samples.head(20))

# counting douplicates

count = Counter()
for row in duplicate_samples['Grouped']:
	row_list = row.split(',')
	count.update(Counter(combinations(row_list, 2)))

print(count.most_common(10))


# what product sold the most

product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']
print(product_group.sum())

# plot

products = [product for product, df in product_group]
plt.bar(products, quantity_ordered)
plt.xticks(products, rotation='vertical', size=8)
plt.xlabel('Product Name.')
plt.ylabel('Quantity.')
plt.show()



prices = all_data.groupby('Product').mean()['Price Each']
print(prices)
fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered)
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price $', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)
plt.show()

