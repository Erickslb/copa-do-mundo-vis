import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

df_final = pd.read_csv("df_final.csv")

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
col1, col2= st.columns([1,3])
with col1:
    st.subheader("Análise ao longo do tempo")

with col1:
    st.markdown('Esse gráfico tem como objetivo exibir dados acumulados de cada seleção ao longo do tempo: gols feitos, gols tomados, vitórias e derrotas.')    
    choice = st.selectbox ("O que você quer observar ao longo do tempo?", ["Gols dados", "Gols recebidos", "Vitórias", "Derrotas"])
with col2:
    plot_filtro(df_final, choice)



### ANÁLISE POR SELEÇÃO ###
col3, col4= st.columns([1,3])
with col3:
    st.subheader("Análise por seleção")

with col3:
    st.markdown('Esse gráfico tem como objetivo exibir dados acumulados de cada seleção ao longo do tempo: gols feitos, gols tomados, vitórias e derrotas.')    
    analise = st.selectbox ("O que você quer analisar?", ["Gols dados", "Gols recebidos", "Vitórias", "Derrotas"])
    copa = st.selectbox ("Qual a estatística?", ["Média", "Mediana", "Variância"])
with col4:
    #plot_filtro(df_final, choice)
    df = df_final.groupby(['team','year']).score.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])

    st.bar_chart(chart_data)
    #fig = px.line(df, x='year', y=df.columns[1:-1])
    #st.plotly_chart(fig, use_container_width=False)