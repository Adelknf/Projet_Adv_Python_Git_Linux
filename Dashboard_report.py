# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 23:07:19 2025

@author: Adel Khennouf
"""

import pandas as pd
import dash
import dash_table
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import datetime

# Fichiers CSV
CSV_FILE = "/home/ubuntu/Projet_Adv_Python_Git_Linux/prix_societe_generale.csv"
DAILY_FILE = "/home/ubuntu/Projet_Adv_Python_Git_Linux/donnees_jour.csv"
HISTORICAL_FILE = "/home/ubuntu/Projet_Adv_Python_Git_Linux/prix_societe_generale.csv"
REPORT_FILE = "/home/ubuntu/Projet_Adv_Python_Git_Linux/rapport.csv"

def get_last_price():
    """Récupère la dernière valeur du prix depuis le fichier CSV."""
    try:
        df = pd.read_csv(CSV_FILE, sep=";")
        
        last_price = df.iloc[-1][" Prix (Euro)"]  # Dernière ligne
        return f"Prix actuel : €{last_price}"
    except FileNotFoundError:
        return "Aucune donnée disponible."
    except Exception as e:
        return f"Erreur : {e}"

def load_csv(file_path):
    """Charge un CSV et formate la colonne 'Heure'."""
    try:
        df = pd.read_csv(file_path, sep=";")
        df.rename(columns={"Heure (Europe/Paris)": "Heure"}, inplace=True)
        df["Heure"] = pd.to_datetime(df["Heure"], format="%Y-%m-%d %H:%M:%S")
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Heure", "Prix (Euro)"])

def get_daily_report():
    """Charge et affiche les statistiques du rapport quotidien."""
    try:
        df = pd.read_csv(REPORT_FILE, sep=";")
        df.columns = df.columns.str.strip()
        return df.tail(1)  # Récupérer la dernière ligne du rapport
    except FileNotFoundError:
        return pd.DataFrame(columns=["Min", "Max", "Ouverture", "Fermeture", "Volatilité"])

# Initialisation de Dash
app = dash.Dash(__name__)

# Mise en page du Dashboard
app.layout = html.Div([
    html.H1("📊 Suivi du Prix – Société Générale"),
    
    html.H3(id="last-price", style={"textAlign": "center", "color": "black"}),  # Prix actuel
    
    html.H4("📅 Évolution du prix du jour"),
    dcc.Graph(id="daily-chart"),  # Graphique du jour
    
    html.H4("📜 Évolution du prix historique"),
    dcc.Graph(id="historical-chart"),  # Graphique historique
    
    html.H4("📑 Rapport quotidien"),
    dash_table.DataTable(
        id="daily-report",
        columns=[{"name": col, "id": col} for col in ["Min", "Max", "Ouverture", "Fermeture", "Volatilité"]],
        style_table={"margin": "auto", "width": "50%"},
        style_cell={"textAlign": "center", "padding": "10px", "fontSize": "18px"},
    ),
    
    dcc.Interval(id="update-interval", interval=5000, n_intervals=0)  # Mise à jour automatique
])

@app.callback(
    Output("last-price", "children"),
    Output("daily-chart", "figure"),
    Output("historical-chart", "figure"),
    Output("daily-report", "data"),
    Input("update-interval", "n_intervals")
)
def update_dashboard(_):
    """Met à jour le prix, les graphiques et le rapport quotidien."""
    last_price_text = get_last_price()
    df_daily = load_csv(DAILY_FILE)
    df_historical = load_csv(HISTORICAL_FILE)
    df_report = get_daily_report()
    
    fig_daily = px.line(df_daily, x="Heure", y=" Prix (Euro)", title="Prix du jour")
    fig_historical = px.line(df_historical, x="Heure", y=" Prix (Euro)", title="Prix historique")

    return last_price_text, fig_daily, fig_historical, df_report.to_dict("records")

# Exécution du serveur
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)
