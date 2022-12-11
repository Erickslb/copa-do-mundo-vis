import streamlit as st
import pandas as pd
import plotly.express as px

df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
fig = px.pie(df, values='pop', names='country', title='Population of European continent')

df_gols = pd.read_csv("dados_copa.csv")
st.write("Hello World")


st.line_chart(df)
st.sidebar.success("Select a demo above.")

#filtro
choice = st.sidebar.selectbox("Filtrar por", ["gols", "vitórias", "derrotas"])

#grafico filtrado
if choice == "gols":
    st.line_chart(df_gols)
else:
    #st.line_chart(df)
    fig = px.line(df_gols, x='year', y=df_gols.columns)
    #st.plotly_chart(fig, use_container_width=True)
    
