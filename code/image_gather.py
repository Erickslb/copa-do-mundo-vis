#%%
import plotly.express as px
import pandas as pd
from skimage import io

bandeiras = pd.read_csv("https://raw.githubusercontent.com/programacaodinamica/analise-dados/master/dados/countries-fifa-flags.csv")
campeoes = pd.read_csv("./campeoes.csv")
#%%

def select_winner(year):
    winner = campeoes[campeoes['year'] == year]['team'].tolist()[0]
    url = bandeiras[bandeiras['country']== winner]['url'].tolist()[0]
    return [winner, url]

for i in campeoes['year'].unique().tolist()[:-1]:
    winner_url = select_winner(i)
    
    image = io.imread(winner_url[1])

    folder = '../img/'
    png = '.png'

    dir_string = folder+winner_url[0]+png
    
    io.imsave(dir_string, image)

