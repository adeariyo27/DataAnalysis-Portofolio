# -*- coding: utf-8 -*-
"""Data Manipulation - Sales performance in each branch

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12OJU6iDA6W_tnVeoB8wzpZoMXNEPboKr

# Retail Sales Performance Dataset For Each quarter
The company needs a comparison of the performance of each branch in various cities in 2019. Samples will be collected from the five major cities on the island of Java to be described in terms of order size, number of consumers, number of items, number of brands, and GMV every month.

This is 4 csv files containing retail data for each quarter:
*   (Data from January - March) --> https://storage.googleapis.com/dqlab-dataset/10%25_original_randomstate%3D42/retail_data_from_1_until_3_reduce.csv
*   (Data from April - June) --> https://storage.googleapis.com/dqlab-dataset/10%25_original_randomstate%3D42/retail_data_from_4_until_6_reduce.csv
*   (Data from July - September) --> https://storage.googleapis.com/dqlab-dataset/10%25_original_randomstate%3D42/retail_data_from_7_until_9_reduce.csv
*   (Data from October - December) --> https://storage.googleapis.com/dqlab-dataset/10%25_original_randomstate%3D42/retail_data_from_10_until_12_reduce.csv
"""

import pandas as pd
import matplotlib.pyplot as plt

"""### [1]. Load each *.csv data with Pandas"""

retail_data1 = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/10%25_original_randomstate%3D42/retail_data_from_1_until_3_reduce.csv')
retail_data2 = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/10%25_original_randomstate%3D42/retail_data_from_4_until_6_reduce.csv')
retail_data3 = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/10%25_original_randomstate%3D42/retail_data_from_7_until_9_reduce.csv')
retail_data4 = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/10%25_original_randomstate%3D42/retail_data_from_10_until_12_reduce.csv')

"""### [2]. Data validation and transformation
* View the top 5 data.
* Examine the column list for all data frames to see if all of the columns from the four different data frames have the same structure.
* If the structure is the same, they are combined.
* Examine the merged data frame information.
* Print statistics for merged data frames.





"""

print('PENGECEKAN DATA\n\n')

print(retail_data1.head())

print('Kolom retail_data1: %s' %retail_data1.columns)
print('Kolom retail_data2: %s' %retail_data2.columns)
print('Kolom retail_data3: %s' %retail_data3.columns)
print('Kolom retail_data4: %s' %retail_data4.columns)

retail_table = pd.concat([retail_data1,retail_data2,retail_data3,retail_data4])
print('\nJumlah baris:', retail_table.shape[0])

print('\nInfo:')
print(retail_table.info())

print('\nStatistik deskriptif:\n', retail_table.describe())

"""### [3]. Data Transformation

* If there is data that is not appropriate, it can be discarded.
* If there is a column that should be of type **datetime64**, change it.
* Double-check the data frame information.
* Print descriptive statistics from the data frame.
"""

print('TRANSFORMASI DATA\n\n')

cek = retail_table.loc[(retail_table['item_price'] < 0) | retail_table['total_price'] < 0]
print('\nitem_price < 0 atau total_price < 0:\n', cek)
if cek.shape[0] != 0:
	retail_table = retail_table.loc[(retail_table['item_price'] > 0) & (retail_table['total_price'] > 0)]

cek = retail_table.loc[retail_table['order_id'] == 'undefined']
print('\norder_id yang bernilai undefined:\n', cek)
if cek.shape[0] != 0:
	retail_table = retail_table.loc[retail_table['order_id'] != 'undefined']

retail_table['order_id'] = retail_table['order_id'].astype('int64')
retail_table['order_date'] = pd.to_datetime(retail_table['order_date'])
print('\nInfo:')
print(retail_table.info())

print('\nStatistik deskriptif:\n', retail_table.describe())

"""### [4]. Limit provinces on the island of Java to only five major provinces (DKI Jakarta, West Java, Central Java, East Java, and Yogyakarta).

"""

print('\nFILTER 5 PROVINCE TERBESAR DI PULAU JAWA\n')
java = ['DKI Jakarta','Jawa Barat','Jawa Tengah','Jawa Timur','Yogyakarta']
retail_table = retail_table.loc[retail_table['province'].isin(java)]
print(retail_table['province'].unique())

"""### [5]. Group data based on filtered **order_date** and **province**, then calculate unique order count, unique customer count, unique product count, unique brand count, and GMV (Gross Merchandise Volume = total_price for all sales)."""

groupby_city_province = retail_table.groupby(['order_date','province']).agg({
   'order_id': 'nunique',
   'customer_id': 'nunique',
   'product_id': 'nunique',
   'brand': 'nunique',
   'total_price': sum
})

groupby_city_province.columns = ['order','customer','product','brand','GMV']
print('\ngroupby_city_province (10 data teratas):\n', groupby_city_province.head(10))

"""### [6]. Unstack to get **order_date** in the row and **province** in the column."""

unstack_city_province = groupby_city_province.unstack('province').fillna(0)
print('\nunstack_city_province (5 data teratas):\n', unstack_city_province.head())

"""### [7]. Slicing data for each measurement (column) for example: **order** column."""

idx = pd.IndexSlice
by_order = unstack_city_province.loc[:,idx['order']]
print('\nby order (5 data teratas):\n', by_order.head())

"""### [8]. Perform resampling on the data to carry out monthly calculations."""

by_order_monthly_mean = by_order.resample('M').mean()
print('\nby_order_monthly_mean (5 data teratas):\n', by_order_monthly_mean.head())

"""### [9]. Create a Plot from step 8"""

by_order_monthly_mean.plot(
   figsize = (8,5),
   title = 'Average Daily Order Size in Month View for All Province'
)
plt.ylabel('avg order size')
plt.xlabel('month')
plt.show()

"""### [10]. Create an automation for each measurement (column)
Steps 7 through 9 have only been completed for one measurement, the order column. That means four more instances of code like this must be written. Because the coding structure remains the same, we may use repetition based on the number of measurements, precisely 5, to display the five measurements graphically in a single canvas figure.

"""

fig, axes = plt.subplots(5, 1, figsize=(8, 25))

idx = pd.IndexSlice
for i, measurement in enumerate(groupby_city_province.columns):
    by_measurement = unstack_city_province.loc[:,idx[measurement]]
    by_measurement_monthly_mean = by_measurement.resample('M').mean()
    by_measurement_monthly_mean.plot(
        title = 'Average Daily ' + measurement + ' Size in Month View for all Province',
        ax = axes[i]
    )
    axes[i].set_ylabel('avg ' + measurement + ' size')
    axes[i].set_xlabel('month')

plt.tight_layout()
plt.show()