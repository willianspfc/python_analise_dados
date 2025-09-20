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

