import streamlit as st
import pandas as pd
import plotly.express as px

df_final = pd.read_csv("df_final.csv")

st.set_page_config(page_title="My App",layout='wide')

st.sidebar.write("Sidebar")


# somatório de gols dados acumulados
gols_feitos = df_final.groupby(['team','year']).score.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()

# somatório de gols recebidos acumulados
gols_tomados = df_final.groupby(['team','year']).conceded.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()

# somatório das vitórias acumuladas
vitorias = df_final.groupby(['team','year']).wins.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()

# somatório das derrota acumuladas
derrotas = df_final.groupby(['team','year']).losses.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
##INTRODUÇÃO##
st.title('TrabViz - Análise das copas')

### GRÁFICO PRINCIPAL###
col1, col2= st.columns([1,3])
with col1:
    st.subheader("Análise ao longo do tempo")
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 3.3, .4, .2, .2))
with col1:
    st.markdown('Esse gráfico tem como objetivo exibir dados acumulados de cada seleção ao longo do tempo: gols feitos, gols tomados, vitórias e derrotas.')    
    choice = st.selectbox ("O que você quer observar ao longo do tempo?", ["Gols dados", "Gols recebidos", "Vitórias", "Derrotas"])
with col2:
    #grafico filtrado
    if choice == "Gols dados":
        fig = px.line(gols_feitos, x='year', y=gols_feitos.columns[1:-1])
        st.plotly_chart(fig, use_container_width=False)
    elif choice == "Gols recebidos":
        fig = px.line(gols_tomados, x='year', y=gols_tomados.columns[1:-1])
        st.plotly_chart(fig, use_container_width=False)
    elif choice == "Vitórias":
        fig = px.line(vitorias, x='year', y=vitorias.columns[1:-1])
        st.plotly_chart(fig, use_container_width=False)
    elif choice == "Derrotas":
        fig = px.line(derrotas, x='year', y=derrotas.columns[1:-1])
        st.plotly_chart(fig, use_container_width=False)
