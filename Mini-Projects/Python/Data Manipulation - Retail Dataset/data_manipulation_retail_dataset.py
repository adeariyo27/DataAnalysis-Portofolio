# -*- coding: utf-8 -*-
"""Data Manipulation - Retail Dataset

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NEus3pREbQajh9-Ib-cb7VsgZFNgJy3z

#Retail Dataset
From the following dataset: *https://storage.googleapis.com/dqlab-dataset/retail_raw_test.csv*, determine:
*   Read dataset.
*   The data type is changed to the correct type:
 *   **customer_id** from string to int64
 *   **quantity** from string to int64
 *   **item_price** from string to int64
*   Transform **product_value** so that it has a uniform shape with 'PXXXX' format, then assign it to a new column **product_id**. If there is 'NaN' or 'NULL' value, then replace it with 'unknown'. Also, drop the **product_value** column.
*   Transform **order_date** into value in the 'YYYY-mm-dd' format.
*   Check for missing data from each column and then fill in the *missing values*
 *   In **brand** with 'no_brand'
 *   In **city** and **province** with 'unknown'
*   Create column **city/province** from combined **city** and **province**
*   Create index based on **city_provice**, **order_date**, **customer_id**, **order_id**, **product_id**
*   Create a **total_price** column as a result of multiplying **quantity** by **item_price**
*   Slice data for Jan-2019 only
"""

import pandas as pd

print("[1] READ DATASET")
df = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/retail_raw_test.csv', low_memory=False)
print("    Dataset:\n", df.head())
print("    Info:\n", df.info())

print("\n[2] CHANGE DATA TYPE")
df["customer_id"] = df["customer_id"].apply(lambda x: x.split("'")[1]).astype("int64")
df["quantity"] = df["quantity"].apply(lambda x: x.split("'")[1]).astype("int64")
df["item_price"] = df["item_price"].apply(lambda x: x.split("'")[1]).astype("int64")
print("    Tipe data:\n", df.dtypes)

print("\n[3] TRANSFORM product_value INTO product_id")
import math
def impute_product_value(val):
    if math.isnan(val):
        return 'unknown'
    else:
        return 'P' + '{:0>4}'.format(str(val).split('.')[0])

df["product_id"] = df["product_value"].apply(lambda x: impute_product_value(x))
df.drop(["product_value"], axis=1, inplace=True)
print(df.head())

print("\n[4] TRANSFORM order_date INTO 'YYYY-mm-dd' FORMAT")
months_dict = {
   "Jan":"01",
   "Feb":"02",
   "Mar":"03",
   "Apr":"04",
   "May":"05",
   "Jun":"06",
   "Jul":"07",
   "Aug":"08",
   "Sep":"09",
   "Oct":"10",
   "Nov":"11",
   "Dec":"12"
}
df["order_date"] = pd.to_datetime(df["order_date"].apply(lambda x: str(x)[-4:] + "-" + months_dict[str(x)[:3]] + "-" + str(x)[4:7]))
print("    Tipe data:\n", df.dtypes)

print("\n[5] HANDLING MISSING VALUE")
df[["city","province"]] = df[["city","province"]].fillna("unknown")
df["brand"] = df["brand"].fillna("no_brand")
print("    Info:\n", df.info())

print("\n[6] CREATE NEW COLUMN city/province")
df["city/province"] = df["city"] + "/" + df["province"]
df.drop(["city","province"], axis=1, inplace=True)
print(df.head())

print("\n[7] CREATE HIERACHICAL INDEX")
df = df.set_index(["city/province","order_date","customer_id","order_id","product_id"])
df = df.sort_index()
print(df.head())

print("\n[8] CREATE NEW COLUMN total_price")
df["total_price"] = df["quantity"] * df["item_price"]
print(df.head())

print("\n[9] SLICE DATASET FOR ONLY JANUARY 2019")
idx = pd.IndexSlice
df_jan2019 = df.loc[idx[:, "2019-01-01":"2019-01-31"], :]
print("Dataset akhir:\n", df_jan2019)