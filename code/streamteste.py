import streamlit as st
import pandas as pd
import plotly.express as px

df_final = pd.read_csv("df_final.csv")
st.write("Hello World")

# somatório de gols dados acumulados
gols_feitos = df_final.groupby(['team','year']).score.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()

# somatório de gols recebidos acumulados
gols_tomados = df_final.groupby(['team','year']).conceded.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()

# somatório das vitórias acumuladas
vitorias = df_final.groupby(['team','year']).wins.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()

# somatório das derrota acumuladas
derrotas = df_final.groupby(['team','year']).losses.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()


#filtro
choice = st.sidebar.selectbox("Filtrar por", ["Gols dados", "Gols recebidos", "Vitórias", "Derrotas"])

#grafico filtrado
if choice == "Gols dados":
    fig = px.line(gols_feitos, x='year', y=gols_feitos.columns[1:-1])
    st.plotly_chart(fig, use_container_width=True)
elif choice == "Gols recebidos":
    fig = px.line(gols_tomados, x='year', y=gols_tomados.columns[1:-1])
    st.plotly_chart(fig, use_container_width=True)
elif choice == "Vitórias":
    fig = px.line(vitorias, x='year', y=vitorias.columns[1:-1])
    st.plotly_chart(fig, use_container_width=True)
elif choice == "Derrotas":
    fig = px.line(derrotas, x='year', y=derrotas.columns[1:-1])
    st.plotly_chart(fig, use_container_width=True)

    
