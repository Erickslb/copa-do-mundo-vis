import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import scipy.stats
import plotly.io as pio
from datetime import date, time, datetime
import plotly.graph_objects as go
from skimage import io

import urllib.request
from PIL import Image

bandeiras = pd.read_csv("https://raw.githubusercontent.com/programacaodinamica/analise-dados/master/dados/countries-fifa-flags.csv")
campeoes = pd.read_csv("./code/campeoes.csv")
df_copa = pd.read_csv("./code/df_copas.csv")
df_final = pd.read_csv("./code/df_final.csv")


st.set_page_config(page_title='Copa do Mundo - Vis',
                   layout="wide", page_icon=":soccer:")


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


def line_plot(df, choice):
    if choice == "Gols feitos":
        df_choice = df.groupby(['team','year']).score.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    elif choice == "Gols tomados":
        df_choice = df.groupby(['team','year']).conceded.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    elif choice == "Vitórias":
        df_choice = df.groupby(['team','year']).wins.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    elif choice == "Derrotas":
        df_choice = df.groupby(['team','year']).losses.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    
    fig = px.line(df_choice, x='year', y=df_choice.columns, width=700, height=500)
    
    fig.update_layout(xaxis_title="Ano",
        yaxis_title=choice,
        legend_title="País")
    st.plotly_chart(fig, use_container_width=False)


def line_plot_modified(df, choice, teams):
    if choice == "Gols feitos":
        df_choice = df.groupby(['team','year']).score.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    elif choice == "Gols tomados":
        df_choice = df.groupby(['team','year']).conceded.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    elif choice == "Vitórias":
        df_choice = df.groupby(['team','year']).wins.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    elif choice == "Derrotas":
        df_choice = df.groupby(['team','year']).losses.sum().unstack().fillna(0).cumsum(axis=1).T.reset_index()
    
    fig = px.line(df_choice, x='year', y=teams, width= 700, height=500)
    
    fig.update_layout(xaxis_title="Ano",
        yaxis_title=choice,
        legend_title="País")
    st.plotly_chart(fig, use_container_width=False)

def third_plot(df, analise, teams):
    # processando dados (gols feitos)
    home_scores = df[['home_team', 'home_score', 'year']].rename({'home_team':'team', 'home_score':'score'}, axis='columns')
    away_scores = df[['away_team', 'away_score', 'year']].rename({'away_team':'team', 'away_score':'score'}, axis='columns')
    feitos = pd.concat([home_scores, away_scores]).reset_index(drop=True).fillna(0)

    # processando (gols tomados)
    home_conceded = df[['home_team', 'away_score', 'year']].rename({'home_team':'team', 'away_score':'conceded'}, axis='columns')
    away_conceded = df[['away_team', 'home_score', 'year']].rename({'away_team':'team', 'home_score':'conceded'}, axis='columns')
    tomados = pd.concat([home_conceded, away_conceded]).reset_index(drop=True).fillna(0)
    # analise
    if analise == "Gols feitos":
        df_choose = feitos
        value = "score"
    elif analise=="Gols tomados":
        df_choose = tomados
        value = "conceded"

    df_choose = df_choose[df_choose['team'].isin(teams)].reset_index(drop = True)
    
    fig = px.box(df_choose,  x='team', y=value, width= 700, height=500)
    fig.update_layout(
    xaxis_title="Seleção",
    yaxis_title=analise)
    fig.update_traces(marker_color='#22A39F')
    st.plotly_chart(fig, use_container_width=False)
    

def plot_champion_image(team):
    img_dir = './img/' + team + '.png'
    img = io.imread(img_dir)
    fig = px.imshow(img)

    fig.update_layout(xaxis=dict(showgrid=False),
              yaxis=dict(showgrid=False)
    )

    fig.update_xaxes(visible=False)   
    fig.update_yaxes(visible=False)

    fig.update_layout(
    title={
        'text': f"Campeão: {team}",
        'y':0.2,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

    st.plotly_chart(fig,use_container_width=True)

def get_teams_options(df):
    options = df['team'].unique().tolist()
    return options



# ---- SIDEBAR -----


st.sidebar.image('./img/worldcup.png', width=250, output_format='png')

st.sidebar.text("")
st.sidebar.text("")

st.sidebar.subheader("Filtros:")

anos_copas = get_unique_years(df_copa)  
ano_comeco, ano_final = st.sidebar.select_slider('Selecione os anos que você deseja incluir', anos_copas, [1930, 2022])

df_filtered_slider = filter_years(df_final)

all_teams_selected = st.sidebar.selectbox('Você deseja selecionar somente seleções específicas?', ['Incluir todas as seleções','Selecionar times manualmente (Escolhas abaixo)'])
if (all_teams_selected == 'Selecionar times manualmente (Escolhas abaixo)'):
    choice_teams = st.sidebar.multiselect("Que seleções você quer selecionar?",
    options = get_teams_options(df_filtered_slider), 
    default = get_teams_options(df_filtered_slider))



# ---- Principal -----

## INTRODUÇÃO 

col0_introduction0, col1_introduction0 = st.columns((8,4))
with col0_introduction0:
    st.title('Copas do Mundo - Visualização da Informação')

with col1_introduction0:
    st.text("")
    st.text("")
    st.markdown("[Repositório no Github](https://github.com/Erickslb/copa-do-mundo-vis)")

col0_introduction1, col1_introduction1 = st.columns((8,2))

with col0_introduction1:
    st.markdown("A Copa do Mundo é um campeonato mundial de futebol, que acontece a cada quatro anos e é organizada pela FIFA (Federação Internacional de Futebol). Nações de todos os continentes passam por jogos eliminatórios para se classificar e poder disputar a taça. Esse é o campeonato mais aguardado por amantes do esporte, nele está presente o mais alto nível de futebol.")
    st.markdown("Você já se interessou alguma vez por saber quais seleções são campeãs das Copas do Mundo da FIFA ou quem são as seleções que mais se destacam nesse campeonato e não teve paciência para procurar? Se sim, esse é o app certo para você: Você pode verificar os campeões anteriores facilmente e além disso pode ver as campanhas das seleções ao longo de todas as Copas.")


## Dados selecionados pelo filtro de anos

col0_data0, col1_data0 = st.columns((8,2))

with col0_data0:
    st.subheader("Dados selecionados")
    st.markdown("Fonte dos dados utilizados no projeto: [International football results from 1872 to 2022](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017?select=results.csv)")
    st.markdown("Aqui você pode ver os dados selecionados após a filtragem no slider da barra lateral")
    
see_data = st.expander('Você pode clicar aqui para ver os dados utilizados')
filtered_data = filter_years(df_copa)
with see_data:
    st.dataframe(data=filtered_data)


### Campeões das copas do mundo

col0_0, col1_0, col2_0, col3_0 = st.columns((3,0.55,5,3))

with col0_0:
    st.subheader("Campeões")
    st.markdown("Quer saber qual o campeão da copa do mundo de algum ano específico?")
    year_wanted = st.selectbox("Selecione o ano",anos_copas[:-1])
    winner = select_winner(year_wanted)
    
with col2_0:
    plot_champion_image(winner[0])

with col3_0:
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")

    stats = champions_stats_catcher(year_wanted)
    st.markdown(f"##### :white_check_mark: **Vitórias**: {stats[0]}")
    st.markdown(f"##### :x: **Derrotas**: {stats[1]}")
    st.markdown(f"##### :soccer: **Gols marcados**: {stats[2]}")
    st.markdown(f"##### 🥅 **Gols tomados**: {stats[3]}")
    


### Análise ao longo do tempo (Sumô)

col1_1, col2_1, col3_1 = st.columns((3,0.5,8))

with col1_1:
    st.subheader("Análise ao longo tempo")
    st.markdown('Esse gráfico tem como objetivo exibir dados acumulados de cada seleção ao longo do tempo: gols feitos, gols tomados, vitórias e derrotas.')    
    choice_what = st.selectbox("O que você quer observar ao longo do tempo?", ["Gols feitos", "Gols tomados", "Vitórias", "Derrotas"])

with col3_1:
    if (all_teams_selected == 'Incluir todas as seleções'):
        line_plot(df_filtered_slider, choice_what)
    else:
        if len(choice_teams) == 0:
            st.warning('Por favor, selecione pelo menos uma seleção')
        else:
            line_plot_modified(df_filtered_slider, choice_what, choice_teams)


col1_2, col2_2, col3_2 = st.columns((3,0.5,8))

with col1_2:
    st.subheader("Análise por seleção")
    st.markdown('Esse gráfico tem como objetivo análisar o desempenho de cada seleção. Qual foi a seleção que fez mais gols em um único jogo? Qual a média de gols das melhores seleções?')    
    analise = st.selectbox ("O que você quer analisar?", ["Gols feitos", "Gols tomados"])



with col3_2:
    if (all_teams_selected == 'Incluir todas as seleções'):
        third_plot(filtered_data, analise, get_teams_options(df_filtered_slider))
    else:
        if len(choice_teams) == 0:
            st.warning('Por favor, selecione pelo menos uma seleção')
        else:
            third_plot(filtered_data, analise, choice_teams)
