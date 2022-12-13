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

def champions_stats_catcher(year):
    winner = select_winner(year)
    winner = winner[0]

    row = (df_final[df_final['year'] == year])
    row = row[row['team']==winner].reset_index()
    
    stats = [row.loc[0,i] for i in ['wins', 'losses', 'score', 'conceded']]

    return stats

champions_stats_catcher(1994)

def plot_filtro(df, choice):
    if choice == "Gols feitos":
        df_choice = df.groupby(['team','year']).score.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    elif choice == "Gols tomados":
        df_choice = df.groupby(['team','year']).conceded.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    elif choice == "Vitórias":
        df_choice = df.groupby(['team','year']).wins.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    elif choice == "Derrotas":
        df_choice = df.groupby(['team','year']).losses.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    
    print(df_choice.columns)
    fig = px.line(df_choice, x='year', y=df_choice.columns)
    #fig.update_traces(hovertemplate='Ano: %{x}<br>' + f'{choice}:' + '%{y}')
    #fig.update_layout(
    #xaxis_title="Ano",
    #yaxis_title=choice,
    #legend_title="País",)
    st.plotly_chart(fig, use_container_width=False)
    


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


### Campeões das copas do mundo
col0_title0, space0 = st.columns((2,2))

with col0_title0:
    st.subheader("Campeões")

col0_0, col1_0space, col2_0, col3_0 = st.columns((2,1,3,4))

with col0_0:
    st.markdown("Selecione o ano da copa do mundo que quer ver")
    year_wanted = st.selectbox("",anos_copas[:-1])
    winner = select_winner(year_wanted)

with col2_0:

    st.image(winner[1], output_format='png', width=300)
    st.text(f"‎ ‎ ‎  ‎  ‎  Campeão: {winner[0]}    ")

with col3_0:
    stats = champions_stats_catcher(year_wanted)
    st.markdown(f"##### :white_check_mark: **Vitórias**: {stats[0]}")
    st.markdown(f"##### :x: **Derrotas**: {stats[1]}")
    st.markdown(f"##### :soccer: **Gols marcados**: {stats[2]}")
    st.markdown(f"##### 🥅 **Gols tomados**: {stats[3]}")
    

# %%

### Análise ao longo do tempo (Sumô)
df_filtered_slider = filter_years(df_final)

col0_title1, space1 = st.columns((2,2))

col0_1, col1_1space, col2_1, col3_1 = st.columns((2,0.2,3,4))

with col0_1:
    st.subheader("Análise ao longo tempo")

with col0_1:
    st.markdown('Esse gráfico tem como objetivo exibir dados acumulados de cada seleção ao longo do tempo: gols feitos, gols tomados, vitórias e derrotas.')    
    choice = st.selectbox ("O que você quer observar ao longo do tempo?", ["Gols feitos", "Gols tomados", "Vitórias", "Derrotas"])
with col2_1:
    plot_filtro(df_filtered_slider, choice)

