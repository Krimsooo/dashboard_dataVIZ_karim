import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import plotly_express as px
import time
from functools import wraps
import streamlit.components.v1 as component
from pandas_profiling import ProfileReport

#---------------------------------------------------------------

#Fonction pour relever le temps d'execution d'une fonction
def timer_func(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        f = open("D:/Karim/Projets/dashboard_karim_abed/log_exec.txt",'a',encoding="utf8")
        mes=f'Function {func.__name__!r} executed in {(t2-t1):.4f}s'
        f.write(mes+" "+"\n")
        f.close()
        return result
    return wrap_func
#---------------------------------------------------------------
@timer_func
@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def read(file_path):
    return pd.read_csv(file_path,low_memory=False)

data=read("D:/Karim/Projets/dashboard_karim_abed/full_2020.csv")
#---------------------------------------------------------------

def trans_type(num_col,type):
    return data[num_col].astype(type)

@timer_func
def titre(titre):
    return st.title(titre)

print(data.isnull().sum())
 
titre("test")
st.write(data.head())
st.write(data.head(2000))