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
import pydeck as pdk

st.set_page_config(page_title="Kar'immobilier",
                   page_icon="🏘️",
                   layout="wide",
                   initial_sidebar_state="auto"
                   )

add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

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
        f = open("D:/Karim/Projets/dashboard_dataVIZ_karim/log_exec.txt",'a',encoding="utf8")
        mes=f'Function {func.__name__!r} executed in {(t2-t1):.4f}s'
        f.write(mes+" "+"\n")
        f.close()
        return result
    return wrap_func
#---------------------------------------------------------------
#Fonction de lecture et de modification du dataset
@timer_func
@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def read_and_transform(file_path):
    data=pd.read_csv(file_path,low_memory=False,sep=",")
    data=data.fillna(0)
    data['date_mutation']=pd.to_datetime(data['date_mutation'])
    data['dom']=data['date_mutation'].map(get_dom)
    data['weekday']=data['date_mutation'].map(get_weekday)
    return data

data=read_and_transform("D:/Karim/Projets/dashboard_dataVIZ_karim/full_2020.csv")
#---------------------------------------------------------------
#Fonction qui permet de changer le type d'une colonne 
@timer_func
@st.cache(allow_output_mutation=True)
def change_type(nom_col,type):
    data[nom_col] = data[nom_col].astype(type)
    return data

#Changement de type des colonnes du dataset
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
change_type("valeur_fonciere",int32)
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
change_type("nombre_pieces_principales",int16)

@timer_func
def aff_titre(titre):
    return st.title(titre)

@timer_func
def aff_text(text):
    return st.text(text)

@timer_func
def aff_write(something):
    return st.write(something)

def checkbox(text):
    return st.checkbox(text)

#Commande pour voir le nombre de champs vide/Nan par colonne
#print(data.isnull().sum())

#Commande pour avoir des infos sur le dataset (type+champs non vides)
print(data.info())
print(data.head(5))

#---------------------------------------------------------------

aff_titre("🏢 Kar'immobilier")

aff_text("Les 5 premières lignes dataset 2020")
aff_write(data.head())
but1=checkbox("Afficher le dataset 2020 complet")
        
if but1:
    aff_write(data)


data_3d=data.sample(73100)

layer = pdk.Layer("GridLayer", 
                  data_3d,
                  pickable=True,
                  extruded=True,
                  cell_size=10000,
                  elevation_scale=500,
                  get_position=["longitude","latitude"],
                  cellSize=90000
)

view_state = pdk.ViewState(zoom=4, 
                           bearing=-25, 
                           pitch=45,
                           longitude=2.21,
                           latitude=46.2322)


# Render
r = pdk.Deck(layers=layer, initial_view_state=view_state)

st.pydeck_chart(r)
#r.to_html("grid_layer.html")
