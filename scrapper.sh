#!/bin/bash

URL="https://www.google.com/finance/quote/GLE:EPA"
CSV_FILE="/home/ubuntu/Projet_Adv_Python_Git_Linux/prix_societe_generale.csv"


DATA=$(curl -s "$URL")

# Extraction du prix
PRICE=$(echo "$DATA" | grep -oP '<div class="YMlKec fxKbKc">€[0-9,\.]+' | sed 's/<div class="YMlKec fxKbKc">//;s/\€//')

# Récupération de l'heure actuelle avec timezone Paris
TIME=$(date +"%Y-%m-%d %H:%M:%S")

# Vérifier si le fichier existe, sinon ajouter l'en-tête
if [ ! -f "$CSV_FILE" ]; then
    echo "Heure (Europe/Paris); Prix (Euro)" > "$CSV_FILE"
fi

# Ajouter la nouvelle entrée
echo "$TIME; $PRICE" >> "$CSV_FILE"

done

