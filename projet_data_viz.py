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
from numpy import datetime64, int16, string_
from numpy import int32
import os
import pydeck as pdk

st.set_page_config(page_title="Kar'immobilier",
                   page_icon="🏘️",
                   layout="wide",
                   initial_sidebar_state="auto"
                   )

st.balloons()
#---------------------------------------------------------------
#Fonction pour relever le temps d'execution d'une fonction
@st.cache()
def timer_func(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        f = open("log_exec.txt",'a',encoding="utf8")
        mes=f'Function {func.__name__!r} executed in {(t2-t1):.4f}s'
        f.write(mes+" "+"\n")
        f.close()
        return result
    return wrap_func
#---------------------------------------------------------------

#Fonction de lecture et de modification du dataset
@timer_func
def get_dom(dt):
  return dt.day

@timer_func
def get_weekday(dt):
  return dt.weekday()

@st.cache(allow_output_mutation=True)
def read_and_transform(file_path):
    data=pd.read_csv(file_path,low_memory=False,sep=",")
    data=data.fillna(0)
    data['date_mutation']=pd.to_datetime(data['date_mutation'])
    data['dom']=data['date_mutation'].map(get_dom)
    data['weekday']=data['date_mutation'].map(get_weekday)
    return data

@timer_func
def read(file_path):
    data=pd.read_csv(file_path,low_memory=False,sep=",")
    return data

#Fonction pour sampler un dataset
@timer_func
@st.cache()
def sample_d(dataset,n):
    return dataset.sample(n)

data=read_and_transform("./full_2020.csv")
data_r2020= read("./datasets/full_2020_1.csv")
#---------------------------------------------------------------

#Fonction qui permet de changer le type d'une colonne 
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


st.markdown("<h1 style='text-align:center'>My Streamlit application</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center'>🏘️ Kar'immobilier 🏘️</h1>", unsafe_allow_html=True)

if checkbox("Afficher les 5 premières lignes du dataset modifié"):
    aff_write(data.head())

if checkbox("Afficher le dataset modifié"):
    aff_write(data)

if checkbox("Afficher le dataset original"):
    aff_write(data_r2020)

@timer_func
def plotterhist(column,bine,rwidth,rang,title,xlabel,ylabel):
    fig,ax= plt.subplots()
    n,bine,patches=ax.hist(column,bins=bine, rwidth=rwidth,range=rang)
    for i in range(len(patches)):
        patches[i].set_facecolor(plt.cm.viridis(n[i]/max(n)))
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)

#------------------------------------------------------------
#Map 3D représentant tous les biens vendus en 2020

st.markdown("<h3 style='text-align:center'>Carte 3D des transactions immobilières en 2020</h3>", unsafe_allow_html=True)

data_3d=sample_d(data,47000)
layer = pdk.Layer("GridLayer", 
                  data_3d,
                  pickable=True,
                  extruded=True,
                  cell_size=10000,
                  elevation_scale=500,
                  get_position=["longitude","latitude"],
                  cellSize=90000)

view_state = pdk.ViewState(zoom=4.5, 
                           bearing=-25, 
                           pitch=45,
                           longitude=2.21,
                           latitude=46.2322)
# Render
r = pdk.Deck(layers=layer, initial_view_state=view_state)
st.pydeck_chart(r)

with st.expander("Voir explications"):
    st.write(""" - La carte ci-dessus permet de voir qu'il y a un grand nombre de transactions immobilières dans la région parisienne par exemple """)
    st.write(" - La répartition des transactions immobilières en France est à peu près uniforme")
#------------------------------------------------------------

#r.to_html("grid_layer.html")

moy=data.groupby('code_postal').mean()
graph=px.bar(moy,y=moy['valeur_fonciere'])
graph.update_layout(
    title={
        'text': "Valeurs foncières moyennes des biens en fonction du code postal",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

option = st.selectbox('Quelles figures voulez-vous voir ?',
                      ["Fréquence de transaction par jour",
                       "Évolution des valeurs foncières sur un échantillon voulu",
                       "Top n des départements ayant la plus grande surface à vendre",
                       "Diagramme circulaire représentant la proportion des valeurs foncières moyennes en fonction de la nature du bien"])

#histo
if option=='Fréquence de transaction par jour':
    plotterhist(data['dom'],30,0.8,(1,30),"Fréquence de transaction par jour","Jours du mois","Fréquence")

#st.line_chart
if option=='Évolution des valeurs foncières sur un échantillon voulu':
    df_line_chart=pd.DataFrame()

    number_min = st.number_input("Insérer la borne inférieure de l'échantillon que vous voulez visualiser",step=1,min_value=0)
    number_max = st.number_input("Insérer la borne supérieure de l'échantillon que vous voulez visualiser",step=1,value=2,max_value=100000)
    
    if number_min>=number_max:
        st.warning('ATTENTION !! borne inférieure >= borne supérieure')
    else:
        df_line_chart['valeur_fonciere']=data['valeur_fonciere'][number_min:number_max]
        df_line_chart = df_line_chart.reset_index(drop=True)
        st.line_chart(df_line_chart['valeur_fonciere'])

#plotly 
if option=='Valeurs foncières globales en fonction du code postale':
    st.plotly_chart(graph)
    with st.expander("Voir explications"):
        st.write("""- Le graphique ci-dessus permet d'avoir une vue globale sur les valeurs foncières suivant les codes postaux""")
        st.write("> Par exemple, on voit clairement que les valeurs foncières dans les départements au-dessus 91 sont plus élevé que la normale")

#slider+plotly
if option=='Top n des départements ayant la plus grande surface à vendre':
    top=st.slider("Top n des départements ayant la plus grande surface de bien", min_value=1, value=10, step=1, max_value=100)

    nature = data.groupby('code_departement')['surface_terrain'].sum().reset_index().sort_values('surface_terrain',ascending = False).head(top)
    nature = nature.rename(columns = {'surface_terrain':'Surface totale',
                                    'code_departement':'Code du département'})
    fig = px.bar(nature, x='Code du département', y='Surface totale')
    fig.update_layout(title="Top"+" "+str(top)+" "+ "des départements ayant la plus grande surface à vendre", title_x=0.5)
    st.plotly_chart(fig)

#pie   
if option=="Diagramme circulaire représentant la proportion des valeurs foncières moyennes en fonction de la nature du bien":
    nb=st.slider("Nombre de type de bien à afficher", min_value=1, value=2, step=1, max_value=6)
            
    aff_text("Nombre de type de bien actuel:"+" "+str(nb))
    nature = data.groupby('nature_mutation')['valeur_fonciere'].mean().reset_index().sort_values('valeur_fonciere',ascending = False).head(nb)
    nature = nature.rename(columns = {'valeur_fonciere':'Proportion de la valeur foncière moyenne',
                                      'nature_mutation':'Type de bien'})
    
    fig = px.pie(nature, values='Proportion de la valeur foncière moyenne', 
                 names='Type de bien')
    fig.update_layout(title="Proportion des"+" "+str(nb)+" "+"types de bien en fonction de la valeur fonciere moyenne", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
    

