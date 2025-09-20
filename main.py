#  __     __     __     __         __         __     ______     __   __   
# /\ \  _ \ \   /\ \   /\ \       /\ \       /\ \   /\  __ \   /\ "-.\ \  
# \ \ \/ ".\ \  \ \ \  \ \ \____  \ \ \____  \ \ \  \ \  __ \  \ \ \-.  \ 
#  \ \__/".~\_\  \ \_\  \ \_____\  \ \_____\  \ \_\  \ \_\ \_\  \ \_\\"\_\
#   \/_/   \/_/   \/_/   \/_____/   \/_____/   \/_/   \/_/\/_/   \/_/ \/_/

# Autor: Seu Nome Completo
# Data: 20/09/25 
# Version: 1.0.0

from flask import Flask , request , jsonify, render_template_string
import pandas as pd
import sqlite3
import os
import plotly.graph_objs as go
from dash import Dash , html , dcc
import numpy as np
import config        # Nosso config.py
from sklearn.cluster import KMeans   
from sklearn.preprocessing import StandardScaler

app = Flask (__name__)
pasta = config.FOLDER
caminhoBD = config.DB_PATH
rotas = config.ROTAS
vazio = 0

def init_db():
    with sqlite3.connect(f'{pasta}{caminhoBD}') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inadimplencia(
                mes TEXT PRIMARY KEY,
                inadimplencia REAL)
                       ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selic(
                mes TEXT PRIMARY KEY,
                selic_diaria REAL)
                       ''')
        conn.commit()

@app.route(rotas[0])
def index():
    return render_template_string(f'''
        <h1> Upload de dados Economicos </h1>
        <form action= "{rotas[1]}" method="POST" enctype="multipart/form-data">
            <label for="campo_inadimplencia"> Arquivo de Inadimplencia (CSV): </label>
            <input name="campo_inadimplencia" type="file" required><br>              

            <label for="campo_selic"> Arquivo de Taxa Selic (CSV): </label>
            <input name="campo_selic" type="file" required><br>       

            <input type="submit" value="Fazer Upload"><br>   
        </form>
        <br><br>
        <a href="{rotas[2]}"> Consultar dados Armazenados </a><br>
        <a href="{rotas[3]}"> Visualizar Graficos </a><br>
        <a href="{rotas[4]}"> Editar Inadimplencia </a><br>        
        <a href="{rotas[5]}"> Analisar Correlação </a><br>                                         
                                  ''')

@app.route(rotas[1],methods=['POST','GET'])
def upload():
    inad_file = request.files.get('campo_inadimplencia')
    selic_file = request.files.get('campo_selic')

    if not inad_file or not selic_file : 
        return jsonify ({"Erro":"Ambos os arquivos devem ser enviados"}), 406
    
    inad_df = pd.read_csv(
        inad_file,
        sep = ';',
        names = ['data','inadimplencia'],
        header = 0
    )

    selic_df = pd.read_csv(
        selic_file,
        sep = ';',
        names = ['data','selic_diaria'],
        header = 0
    )
    inad_df['data'] = pd.to_datetime(
        inad_df['data'],
        format='%d/%m/%Y'  )
    selic_df['data'] = pd.to_datetime(
        selic_df['data'],
        format='%d/%m/%Y')
    
    inad_df['mes'] = inad_df['data'].dt.to_period('M').astype(str).drop_duplicates()
    selic_df['mes'] = selic_df['data'].dt.to_period('M').astype(str)

    #inad_df['mes'] = inad_df[['mes','inadimplencia']].drop.duplicates()
    selic_mensal = selic_df.groupby('mes')['selic_diaria'].mean().reset_index()

    with sqlite3.connect(f'{pasta}{caminhoBD}') as conn:
        inad_df.to_sql(
            'inadimplencia',
            conn,
            if_exists = 'replace',
            index = False
        )
        selic_df.to_sql(
            'selic',
            conn,
            if_exists = 'replace',
            index = False
        )
    return jsonify({"Mensagem":"Dados cadastrados com sucesso"}),200

@app.route(rotas[2], methods=['POST','GET'])
def consultar():
    if request.method =="POST":
        tabela = request.form.get("campo_tabela")
        if tabela not in ['inadimplencia','selic']:
            return jsonify({"Erro":"Tabela é invalida"}),400
        with sqlite3.connect(f'{pasta}{caminhoBD}') as conn:
            df = pd.read_sql_query(f'SELECT * FROM {tabela}',conn)
        return df.to_html(index=False) 

    return render_template_string(f'''
        <h1> Consuta de Tabelas </h1>
        <form method="POST">
            <label for="campo_tabela"> Escolha uma tabela: </label>
            <select name="campo_tabela">
                <option value="inadimplencia"> Inadimplencia </option>
                <option value="selic"> Taxa Selic </option>
                <option value="usuarios"> Usuarios </option>
            </select>
            <input type="submit" value="Consultar">
        </form>
        <br>
        <a href="{rotas[0]}"> Voltar </a>
                                  ''')

@app.route(rotas[4],methods=['POST','GET'])
def editar_inadimplencia():

    if request.method == "POST":
        mes = request.form.get('campo_mes')
        novo_valor = request.form.get('campo_Valor')
        try:
            novo_valor = float(novo_valor)
        except:
            return jsonify({"Erro:":"Valor invalido"}),418
        with sqlite3.connect(f'{pasta}{caminhoBD}') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE inadimplencia
            SET inadimplencia = ?
            WHERE mes = ?               
                       ''',(novo_valor,mes))
            conn.commit()
        return jsonify({"Mensagem:":f"Valor atualizado para o mes {mes}"})


    return render_template_string(f'''
        <h1> Editar Inadimplencia </h1>
        <form method="POST">
            <label for="campo_mes"> Mês (AAAA-MM) </label>
            <input type="text" name="campo_mes"><br>

            <label for="campo_valor"> Novo Valor </label>
            <input type="text" name="campo_Valor"><br>
                                  
            <input type="submit" value="Salvar">
        </form>
        <br>
        <a href="{rotas[0]}"> Voltar </a>                         
                                  ''')

@app.route(rotas[5])
def correlacao():
    with sqlite3.connect(f'{pasta}{caminhoBD}') as conn:
        inad_df = pd.read_sql_query("SELECT * FROM inadimplencia",conn)
        selic_df = pd.read_sql_query("SELECT * FROM selic",conn)

    #realiza uma junção entre os dois dataframes usando a coluna de mes como chave
    merged = pd.merge(inad_df,selic_df , on='mes')

    #calcula o coeficiente da correlacao de pearson entre as duas variaveis
    correl = merged['inadimplencia'].corr(merged['selic_diaria'])

    #registra as variaveis para a regressao linear onde x é a variavel
    #independente e y é a variavel dependente
    x = merged['selic_diaria']
    y = merged['inadimplencia']
    #calcula o coeficiente da reta de regressão linear onde M é a inclinação e B é a intersecção
    m,b = np.polyfit(x,y,1)

    # Oba!!! Graficos ☺☻♥
    fig = go.Figure()
    fig.add_trace(go.scatter(
            x = x,
            y = y,
            mode = 'markers',
            name = 'Inadimplencia X Selic',
            marker = dict(                                                        
            color = 'rgba(0,123,255,0.8)',
                size = 12,
                line = dict(width = 2, color = 'white'),
                symbol = 'circle'
            ),
            hovertemplate = 'Selic:%{x:2f}% <br> Inadimplencia: %{Y:.2f}% <extra></extra>'

    ))
    fig.add_trace(go.scatter(
        x=x,
        y=m*x+b,
        mode ='lines',
        line = dict(
            color = 'rgba(255,53,69,1)',
            width = 4,
            dash ='dot'
        )
    ))    
    fig.update_layout(
        title = {
            'text':f'<b> Correlação entre selic e Inadimplencia </b><br><span style="font-size:16px;"> Coeficiente de Correlação {correl:.2f}</span>',          
            'y':0.095,
            'x':0.5,
            'xanchor':'center',
            'yanchor':'top'
        },
        xaxis_title = dict(
            text = 'SELIC Média Mensal (%)',
            font = dict(
                size=18,
                family='Arial',
                color='gray'
            )
        ),
        yaxis_title = dict(
            text = 'Inadimplencia (%)',
            font = dict(
                size=18,
                family='Arial',
                color='gray'
        ),
        xaxis = dict(
            tickfont = dict(
                size=14,
                family='Arial',
                color='black'),
            gridcolor = 'lightgray'
            )
        ),
        yaxis = dict(
            tickfont = dict(
                size=14,
                family='Arial',
                color='black'),
            gridcolor = 'lightgray'
            ),
        font = dict(
                size=14,
                family='Arial',
                color='black',
        ),
        legend = dict(
            orientation = 'h',
            yanchor = 'bottom',
            xanchor = 'center',
            x   = 0.5,  
            y   = 1.05,
            bgcolor = 'rgba(0,0,0,0)',
            borderwidth = 0
        ),
        margin = dict(l=60 , r=60, t=120 , b=60),
        plot_bgcolor = '#f8f9fa',
        paper_bgcolor = 'white'
    )    
    graph_html = fig.to_html(
        full_html = False,
        include_plotlyjs = 'cdn'
    )
    return render_template_string('''
        <html>
            <head>
                <title>Correlação Selic X Inadimplencia</title>
            </head>
            <body>
                <h1>Correlação Selic X Inadimplencia</h1>
                <div>{{grafico|safe}}</div>
                <br>
                <a href="{{ voltar }}"> Voltar </a>
            </body>
        </html>                          ''',grafico = graph_html, voltar = rotas[0])

if __name__ == '__main__':
    app.run(
        debug = config.FLASK_DEBUG,
        host = config.FLASK_HOST,
        port = config.FLASK_PORT
    )

