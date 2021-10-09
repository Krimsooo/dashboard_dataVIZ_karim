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
from numpy import datetime64, int16
from numpy import int32
import os

def get_dom(dt):
  return dt.day

def get_weekday(dt):
  return dt.weekday()
#---------------------------------------------------------------

#Fonction pour relever le temps d'execution d'une fonction
def timer_func(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        f = open("dashboard_dataVIZ_karim/log_exec.txt",'a',encoding="utf8")
        mes=f'Function {func.__name__!r} executed in {(t2-t1):.4f}s'
        f.write(mes+" "+"\n")
        f.close()
        return result
    return wrap_func
#---------------------------------------------------------------
@timer_func
@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def read_and_transform(file_path):
    data=pd.read_csv(file_path,low_memory=False,sep=",")
    data=data.fillna(0)
    data['date_mutation']=pd.to_datetime(data['date_mutation'])
    data['dom']=data['date_mutation'].map(get_dom)
    data['weekday']=data['date_mutation'].map(get_weekday)
    return data

data=read_and_transform("dashboard_dataVIZ_karim/full_2020.csv")
#---------------------------------------------------------------
@timer_func
@st.cache(allow_output_mutation=True)
def change_type(nom_col,type):
    data[nom_col] = data[nom_col].astype(type)
    return data

change_type("id_mutation",str)

change_type("code_commune",str)
change_type("nom_commune",str)
change_type("code_postal",int32)
change_type("nature_mutation",str)
change_type("type_local",str)
change_type("code_nature_culture",str)
change_type("nature_culture",str)
change_type("nature_culture_speciale",str)
change_type("dom",int16)
change_type("surface_terrain",int32)
change_type("surface_reelle_bati",int32)
change_type("nombre_pieces_principales",int16)
change_type("numero_disposition",int16)
change_type("adresse_numero",int16)
change_type("nombre_lots",int16)
change_type("code_type_local",int16)
change_type("weekday",int16)
change_type("code_departement",str)
change_type("adresse_code_voie",str)
change_type("id_parcelle",str)
change_type("code_nature_culture",str)
change_type("adresse_nom_voie",str)

@timer_func
def titre(titre):
    return st.title(titre)
#print(data.isnull().sum())

print(data.info())
titre("test")
st.write(data)