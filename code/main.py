#%%
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import scipy.stats
import plotly.io as pio
from datetime import date, time, datetime
import plotly.graph_objects as go

#%%

bandeiras = pd.read_csv("https://raw.githubusercontent.com/programacaodinamica/analise-dados/master/dados/countries-fifa-flags.csv")
campeoes = pd.read_csv("https://raw.githubusercontent.com/Erickslb/copa-do-mundo-vis/main/code/campeoes.csv")
df_copa = pd.read_csv("https://raw.githubusercontent.com/Erickslb/copa-do-mundo-vis/main/code/df_copas.csv")
df_final = pd.read_csv("./df_final.csv")


# %%
st.set_page_config(page_title='Copa do Mundo - Vis',
                   layout="wide", page_icon=":soccer:")

# %%
# ---- Funções auxiliares ----

def get_unique_years(df):
    return df['year'].unique().tolist()

def filter_years(df):
    years = get_unique_years(df)

    start_index = years.index(ano_comeco)
    final_index = years.index(ano_final)+1

    years_selected = years[start_index:final_index]

    df_filtered_years = df[df['year'].isin(years_selected)].reset_index(drop = True)

    return df_filtered_years

def select_winner(year):
    winner = campeoes[campeoes['year'] == year]['team'].tolist()[0]
    url = bandeiras[bandeiras['country']== winner]['url'].tolist()[0]
    return [winner, url]




#%%

# ---- SIDEBAR -----

st.sidebar.markdown("# Ele gosta")
st.sidebar.image('../img/worldcup.png', width=250, output_format='png')

st.sidebar.text("")
st.sidebar.text("")

st.sidebar.subheader("Filtros:")

#st.sidebar.markdown("**Selecione os anos de Copa do Mundo que você quer analisar:** ")
anos_copas = get_unique_years(df_copa)  
ano_comeco, ano_final = st.sidebar.select_slider('Selecione os anos que você deseja incluir', anos_copas, [1930, 2022])

# %%
# ---- Principal -----

## INTRODUÇÃO 
st.title('Copas do Mundo - Visualização da Informação')

col0_0, col1_space, col2_0, col3_0 = st.columns((2,.3,3,3))

with col0_0:
    st.markdown("### Campeões")
    st.markdown("Selecione o ano da copa do mundo que quer ver")
    year_wanted = st.selectbox("",anos_copas[:-1])
    edilton = select_winner(year_wanted)

with col2_0:
    st.text("")
    st.text("")
    st.image(edilton[1], output_format='png')
    st.text(f"     Campeão: {edilton[0]}    ")

with col3_0:
    st.text("")
    st.text("")
    st.text("")     
    st.markdown("##### Vitórias:")
    st.markdown("##### Derrotas:")
    st.markdown("##### Fallen:")
    st.text(" Fer:")
    
