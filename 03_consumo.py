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
            <li><a href="/grafico3"> Consumo total por Região </a></li>
            <li><a href="/grafico4"> Comparativo entre tipos de bebidas </a></li>
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

@app.route("/grafico3")
def grafico3():
    regioes = {
            "Europa":['France','Germany','Spain','Italy','Portugal'],
            "Asia":['China','Japan','India','Thailand'],
            "Africa":['Angola','Nigeria','Egypt','Algeria'],
            "Americas":['USA','Canada','Brazil','Argentina','Mexico']
             }
    dados = []
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        #itera sobre o dicionario, de regioes onde cada chave (regiao tem uma lista de paises)
        for regiao, paises in regioes.items():
            placeholders = ",".join([f"'{pais}'" for pais in paises])
            query = f"""
                SELECT SUM(total_litres_of_pure_alcohol) As total 
                FROM bebidas
                WHERE country in ({placeholders})                        
                """
            total = pd.read_sql_query(query,conn).iloc[0,0]
            dados.append({
                "Região": regiao,
                "Consumo Total":total})
        dfRegioes = pd.DataFrame(dados)
        figuraGrafico3 = px.pie(
                dfRegioes,
                names = "Região",
                values = "Consumo Total",
                title = "Consumo Total por Região!")
        return figuraGrafico3.to_html()        

@app.route('/comparar',methods=['POST','GET'])
def comparar():
    opcoes = [
        'beer serving',
        'spirit_servings',
        'wine_servings']
    
    if request.method == "POST":
        eixoX = request.form.get('eixo_x')
        eixoY = request.form.get('eixo_y')
        if eixoX == eixoY:
            return"<marquee> Você fez besteira...escolha tabelas diferente...</marquee>" 
        conn = sqlite3.connect(f'{caminho}banco01.bd')
        df = pd.read_sql_query("SELECT country,{},{} FROM bebidas".format(eixoX),(eixoY),conn)
        conn.close()
        figuraComparar = px.scatter(
            df,
            x= eixoX,
            y= eixoY,
            title= f"Comparação entre {eixoX} VS {eixoY}"
        )
        figuraComparar.update_traces(
            textposition = "top center"
        )
        return figuraComparar.to_html()
        
    return render_template_string('''
        <! -- Isso é um comentario em html -->     
        <style>
/* Google Font futurista */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');

body {
    font-family: 'Orbitron', sans-serif;
    background: radial-gradient(circle at top left, #1a1a2e, #0f0f1f, #000);
    color: #e0e0ff;
    padding: 40px;
    display: flex;
    justify-content: center;
    min-height: 100vh;
}

form {
    background: linear-gradient(145deg, #1b1b2f, #23234b);
    padding: 30px 40px;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5), 0 0 20px rgba(138, 43, 226, 0.2);
    width: 100%;
    max-width: 420px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

h2 {
    text-align: center;
    color: #b88aff;
    margin-bottom: 25px;
    font-weight: 600;
    text-shadow: 0 0 8px #8844ff;
}

label {
    display: block;
    margin-top: 20px;
    font-weight: 500;
    color: #cfcfff;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.1);
}

select {
    width: 100%;
    padding: 12px 14px;
    margin-top: 8px;
    border: 1px solid #5a5a89;
    border-radius: 10px;
    background-color: #2b2b4d;
    color: #e0e0ff;
    font-size: 14px;
    box-shadow: inset 0 0 8px rgba(255, 255, 255, 0.05);
    transition: all 0.3s ease;
}

select:focus {
    border-color: #a970ff;
    outline: none;
    box-shadow: 0 0 10px #8844ff;
    background-color: #2f2f5a;
}

input[type="submit"] {
    margin-top: 30px;
    width: 100%;
    background: linear-gradient(145deg, #6c3bd7, #8844ff);
    color: #ffffff;
    border: none;
    padding: 14px;
    font-size: 16px;
    border-radius: 10px;
    cursor: pointer;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: background 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 0 12px rgba(136, 68, 255, 0.5);
}

input[type="submit"]:hover {
    background: linear-gradient(145deg, #7d4eff, #a370ff);
    box-shadow: 0 0 16px rgba(136, 68, 255, 0.8);
}

br {
    display: none;
}

        </style>                                               
        <h2> Comparar Campos </h2>
        <form method="POST">
                                  
            <label for="eixo_x"> Eixo X : </label>
            <select name=""eixo_x>
                {% for opcao in opcoes%}
                   <option value="{{opcao}}"> {{opcao}} </option>
                {% endfor %}
                                  
            </select>
            <br></br>                                        

            <label for="eixo_y"> Eixo Y: </label>
            <select name="eixo_y">
                {% for opcao in opcoes%}
                    <option value="{{opcao}}"> {{opcao}} </option>
                {% endfor %}
                                                 
            </select>
            <br></br> 

        <input type="submit" value=" -- Comparar --">
        </form>
                                  ''',opcoes=opcoes)


## O mundo fica aqui !!!

if __name__ == '__main__':
    criarBandoDados()
    app.run(debug=True)
