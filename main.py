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
                mes TEXT PRIMARY KEY
                inadimplencia REAL)
                       ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selic(
                mes TEXT PRIMARY KEY
                selic_diaria REAL)
                       ''')
        conn.commit()

@app.route(rotas[0])
def index():
    return render_template_string(f'''
        <h1> Upload de dados Economicos </h1>
        <form action= "" method="POST" enctype="multipart/form-data">
            <label for="campo_inadimplencia"> Arquivo de Inadimplencia (CSV): </label>
            <input name="campo_inadimplencia" type="file" required>              

            <label for="campo_selic"> Arquivo de Taxa Selic (CSV): </label>
            <input name="campo_selic" type="file" required>       

            <input type="">                                
                                  ''')