"""
Coinbase Institute
Crypto and The Climate
Date: 
Author: Cesare Fracassi
Twitter: @CesareFracassi
Email: cesare.fracassi@coinbase.com
"""

#%% Import Packages

from os.path import isfile, join
import glob
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt

print("Current Working Directory ", os.getcwd())

#%% Download Market cap data

#%%% Get list of all crypto prices csv files
mypath = r"Data"
filelist = glob.glob(os.path.join(mypath, "*.csv"))

L1_marketcap = pd.DataFrame()
for f in filelist:
    temp = pd.read_csv(f)
    fname = f.split("-")[1][1:-4]
    temp["TICKER"] = fname
    L1_marketcap = L1_marketcap.append(temp)

L1_marketcap["date"] = pd.to_datetime(L1_marketcap["Date"], infer_datetime_format=True)
L1_marketcap["Market Cap"] = (
    L1_marketcap["Market Cap"].replace("[\$,]", "", regex=True).astype(float)
)

#%% Keep obs before March 1, 2022
L1_marketcap = L1_marketcap.loc[
    (L1_marketcap["date"] < "March 1, 2022")
    & (L1_marketcap["date"] > "December 31, 2014")
]

#%% Merge POS or POW data

pospow = pd.read_csv("Data/Layer 1 List.tsv", sep="\t")

L1_marketcap = L1_marketcap.merge(pospow, left_on="TICKER", right_on="TICKER")

#%% Create chart

L1_pospow = L1_marketcap.groupby(["date", "CONS_MECH"])["Market Cap"].sum()
L1_pospow = L1_pospow.unstack(level=-1)
L1_pospow = L1_pospow.divide(L1_pospow.sum(axis=1), axis=0)

fig, ax = plt.subplots()
L1_pospow[["POW", "POW to POS", "POS", "OTHER"]].plot.area(ax=ax, figsize=(12, 8))
ax.legend(title="Consensus")
fig = ax.get_figure()
fig.savefig("PoS-PoW.png")

#L1_pospow[["POW", "POW to POS", "POS", "OTHER"]].to_csv("POS_vs_POW.csv")
