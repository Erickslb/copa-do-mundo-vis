import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

df_final = pd.read_csv("df_final.csv")
copas = pd.read_csv("df_copas.csv")


st.set_page_config(page_title="My App",layout='wide')


st.sidebar.write("Sidebar")

# função para aplicar o filtro e plotar o gráfico principal
def plot_filtro(df_final, choice):
    if choice == "Gols dados":
        df = df_final.groupby(['team','year']).score.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    elif choice == "Gols recebidos":
        df = df_final.groupby(['team','year']).conceded.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    elif choice == "Vitórias":
        df = df_final.groupby(['team','year']).wins.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    elif choice == "Derrotas":
        df = df_final.groupby(['team','year']).losses.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    fig = px.line(df, x='year', y=df.columns[1:-1])
    fig.update_traces(hovertemplate='Ano: %{x}<br>' + f'{choice}:' + '%{y}')
    fig.update_layout(
    xaxis_title="Ano",
    yaxis_title=choice,
    legend_title="País",)
    return st.plotly_chart(fig, use_container_width=False)

##INTRODUÇÃO##
st.title('TrabViz - Análise das copas')

### ANÁLISE POR TEMPO###
col1, col2 = st.columns([1,3])
with col1:
    st.subheader("Análise ao longo do tempo")

with col1:
    st.markdown('Esse gráfico tem como objetivo exibir dados acumulados de cada seleção ao longo do tempo: gols feitos, gols tomados, vitórias e derrotas.')    
    choice = st.selectbox ("O que você quer observar ao longo do tempo?", ["Gols dados", "Gols recebidos", "Vitórias", "Derrotas"])
with col2:
    plot_filtro(df_final, choice)



def plot_filtro2(copas, analise):
    # processando dados (gols feitos)
    home_scores = copas[['home_team', 'home_score', 'year']].rename({'home_team':'team', 'home_score':'score'}, axis='columns')
    away_scores = copas[['away_team', 'away_score', 'year']].rename({'away_team':'team', 'away_score':'score'}, axis='columns')
    feitos = pd.concat([home_scores, away_scores]).reset_index(drop=True).fillna(0)

    # processando (gols tomados)
    home_conceded = copas[['home_team', 'away_score', 'year']].rename({'home_team':'team', 'away_score':'conceded'}, axis='columns')
    away_conceded = copas[['away_team', 'home_score', 'year']].rename({'away_team':'team', 'home_score':'conceded'}, axis='columns')
    tomados = pd.concat([home_conceded, away_conceded]).reset_index(drop=True).fillna(0)
    # analise
    if analise == "Gols feitos":
        df = feitos
        value = "score"
    elif analise=="Gols tomados":
        df = tomados
        value = "conceded"
    
    df = pd.DataFrame(df.reset_index())
    fig = px.box(df.sort_values(by=value,  ascending=False).head(25),  x='team', y=value)
    fig.update_layout(
    xaxis_title="Seleção",
    yaxis_title=analise)
    return st.plotly_chart(fig, use_container_width=False)



### ANÁLISE POR SELEÇÃO ###
col3, col4= st.columns([1,3])
with col3:
    st.subheader("Análise por seleção")

with col3:
    st.markdown('Esse gráfico tem como objetivo exibir dados acumulados de cada seleção ao longo do tempo: gols feitos, gols tomados, vitórias e derrotas.')    
    analise = st.selectbox ("O que você quer analisar?", ["Gols feitos", "Gols tomados"])
    #estatistica = st.selectbox ("Qual a estatística?", ["Valor absoluto","Média", "Máximo", "Variância"])
with col4:
    plot_filtro2(copas, analise)