from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio
import random 
import os

pio.renderers.default = "browser"

caminho = "C:/Users/sabado/Desktop/PYTHON AD WILLIAM MARQUES/"
tabela = ["drinks.csv","avengers.csv"]

codhtml = ''' 
    <h1> Dashboards - Consumo de Alcool   </h1>
    <h2> Parte 01   </h2>
        <ul>
            <li><a href="/grafico1"> Top 10 paises em consumo de alcool </a></li>
            <li><a href="/grafico2"> Media de consumo por tipo </a></li>
            <li><a href="/grafico3> Consumo total por Região </a></li>
            <li><a href="/grafico4> Comparativo entre tipos de bebidas </a></li>
            <li><a href="/pais"> Insights por pais </a></li>
        </ul>
    <h2> Parte 02   </h2>
        <ul>
            <li><a href="/comparar"> Comparar </a></li>
            <li><a href="/upload"> Upload CSV Vingadores </a></li>
            <li><a href="/apagar"> Apagar Tabela </a></li>
            <li><a href="/ver"> Ver Tabela </a></li>
            <li><a href="/vaa"> V.A.A (Vingadores Alcolicos Anonimos) </a></li>
        </ul>
'''

def carregarCsv():
    #carregar o arquivo drinks
    #dfDrinks =  pd.read_csv(r"C:\Users\sabado\Desktop\PYTHON AD WILLIAM MARQUES\drinks.csv")

    try:

        dfDrinks= pd.read_csv(os.path.join(caminho,tabela[0]))
        dfAvengers = pd.read_csv(os.path.join(caminho,tabela[1]),encoding='latin1')
        return dfDrinks , dfAvengers
    except Exception as erro:
        print(f"Erro ao carregar os arquivos csv: {erro}")
        return None , None

def criarBandoDados():
    conn = sqlite3.connect(f"{caminho}banco01.bd")     
    #carregar dados usando nossa função criada anteriormente
    dfDrinks,dfAvengers = carregarCsv() 
    if dfDrinks is None or dfAvengers is None:
        print("Falha ao carregar os dados!")
        return
    #inserir as tabelas no banco de dados
    dfDrinks.to_sql("bebidas",conn,if_exists="replace",index=False)
    dfAvengers.to_sql("vingadores",conn,if_exists="replace",index=False)
    conn.commit()
    conn.close()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(codhtml) 

@app.route('/grafico1')
def grafico1():
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        df = pd.read_sql_query("""
            SELECT country,total_litres_of_pure_alcohol
            FROM bebidas  
            ORDER BY total_litres_of_pure_alcohol DESC
            LIMIT 10                 
                               """,conn)
    figuraGrafico01 = px.bar(
    df,
    x="country",
    y="total_litres_of_pure_alcohol",
    title= "Top 10 paises com maior consumo de alcool"
    )
    return figuraGrafico01.to_html()

@app.route('/grafico2')
def grafico2():
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        df = pd.read_sql_query("""
           SELECT AVG(beer_servings) AS cerveja, AVG(spirit_servings) As destilados , 
                  AVG(wine_servings) AS vinhos FROM bebidas      
                               """,conn) 
    df_melted = df.melt(var_name='Bebidas',value_name='Média de Porções')

    figuraGrafico02 = px.bar(
    df_melted,
    x="Bebidas",
    y="Média de Porções",
    title="Media de consumo global por tipo")
    return figuraGrafico02.to_html()



## O mundo fica aqui !!!

if __name__ == '__main__':
    criarBandoDados()
    app.run(debug=True)
