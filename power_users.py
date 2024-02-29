import pandas as pd
import math
from datetime import datetime

def days_between(d2, d):
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d).days)

def getPowerUsers(data, contract, quantile=0.95, window=30, return_all=False):
    print("preparing data")
    d = data[data["to_address"]==contract]

# calculating recency
    
    def getRecency(date, max_date, window=30):
        return max(0, 1-days_between(date, max_date)/window)
    
    max_date = datetime.strptime(d["date_"].max(), "%Y-%m-%d")

    print("calculating recency")
    recency = pd.DataFrame(d[["from_address", "date_"]].groupby("from_address").max().apply(lambda x: getRecency(x["date_"], max_date, window), axis=1))
    recency.columns=["recency"]

    print("calculating frequency")
# calculating frequency
    frequency = d[["date_","from_address"]].groupby("from_address").nunique().apply(lambda x: x/window)
    frequency.columns=["frequency"]

    print("calculating rfm")
# calculating rfm
    rfm = pd.DataFrame(recency.join(frequency).apply(lambda x: x["recency"]*x["frequency"], axis=1))
    rfm.columns=["rfm_weight"]

    if (return_all):
        return rfm.reset_index()

    print("calculating quantile")
    quant = rfm.quantile(q=quantile)["rfm_weight"]

    print("calculating result")
    result = rfm[rfm["rfm_weight"] >= quant].reset_index()

    return result