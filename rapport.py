# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 14:34:00 2025

@author: Adel Khennouf
"""
import numpy as np
import pandas as pd

# Chargement des données journalières
daily_file = "/home/ubuntu/Projet_Adv_Python_Git_Linux/donnees_jour.csv"
rapport_file = "/home/ubuntu/Projet_Adv_Python_Git_Linux/rapport.csv"

# Lecture des données
df = pd.read_csv(daily_file, sep=";")

# Vérification des données
if df.empty:
    print("Aucune donnée disponible pour aujourd’hui.")
else:
    # Correction des espaces dans le nom de colonne
    df.rename(columns=lambda x: x.strip(), inplace=True)

    # Calcul des log rendements
    df["Rendement_Log"] = np.log(df["Prix (Euro)"] / df["Prix (Euro)"].shift(1))

    # Calcul des statistiques
    min_price = df["Prix (Euro)"].min()
    max_price = df["Prix (Euro)"].max()
    opening_price = df.iloc[0]["Prix (Euro)"]  # Première valeur
    closing_price = df.iloc[-1]["Prix (Euro)"]  # Dernière valeur
    volatilite_journaliere = df["Rendement_Log"].std() * 100  # En %

    # Création du DataFrame du rapport
    rapport_df = pd.DataFrame({
        "Min": [min_price],
        "Max": [max_price],
        "Ouverture": [opening_price],
        "Fermeture": [closing_price],
        "Volatilite": [volatilite_journaliere]
    })

    # Sauvegarde dans un fichier CSV
    rapport_df.to_csv(rapport_file, sep=";", index=False)

