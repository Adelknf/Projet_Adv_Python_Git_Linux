# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 12:17:31 2025

@author: Adel Khennouf
"""
import pandas as pd
import datetime

historical_file = "/home/ubuntu/Projet_Adv_Python_Git_Linux/prix_societe_generale.csv"
daily_file = "/home/ubuntu/Projet_Adv_Python_Git_Linux/donnees_jour.csv"

# Lecture du fichier avec le bon séparateur
df = pd.read_csv(historical_file, sep=";")

# Renommer la colonne pour un accès plus facile
df.rename(columns={"Heure (Europe/Paris)": "Heure"}, inplace=True)

# Conversion en format datetime
df["Heure"] = pd.to_datetime(df["Heure"], format="%Y-%m-%d %H:%M:%S")

# Filtrer entre 9h00 et 17h30
today = datetime.date.today()
start_time = datetime.datetime.combine(today, datetime.time(7, 0))
end_time = datetime.datetime.combine(today, datetime.time(16, 3))

df_filtered = df[(df["Heure"] >= start_time) & (df["Heure"] <= end_time)]

# Sauvegarde du fichier filtré
df_filtered.to_csv(daily_file, sep=";", index=False)



