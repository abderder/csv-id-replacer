import streamlit as st
import pandas as pd
import json

st.title("Anonymisation des données CSV")
data_file = st.file_uploader("Télécharger le fichier JSON avec les informations personnelles : ", type=["json"])
correspondance_file = st.file_uploader("Télécharger le fichier CSV de correspondance : ", type=["csv"])

if data_file is not None and correspondance_file is not None:
    if st.button("Anonymiser les IDs"):
        data_df = data_file.read().decode("utf-8")
        correspondance_df = pd.read_csv(correspondance_file, sep=";")
        # Initialiser la barre de progression
        progress_bar = st.progress(0)
        progress_text = st.empty()
        total_replacements = len(correspondance_df)  # Nombre total d'itérations potentielles
        current_progress = 0
        compteur_remplacement = 0
        remplacements_effectues = []
        for _, row in correspondance_df.iterrows():
            id_ = row['user id']
            email = row['email']
            if f"{id_}" in data_df:
                data_df = data_df.replace(f'{id_}', f'"{email}"')
                compteur_remplacement += 1
                remplacements_effectues.append({"id": id_, "email": email})
            current_progress += 1
            progress_percentage = (current_progress / total_replacements) * 100
            progress_bar.progress(int(progress_percentage))
            progress_text.text(f"Progression : {int(progress_percentage)}%")
        st.write(f"Nombre total de remplacements effectués : {compteur_remplacement}")
        remplacements_df = pd.DataFrame(remplacements_effectues)
        remplacements_csv = remplacements_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger le fichier JSON anonymisé",
            data=data_df,
            file_name="fichier_anonymise.json",
            mime="application/json"
        )
        st.download_button(
            label="Télécharger la liste des emails remplacés avec leurs IDs",
            data=remplacements_csv,
            file_name="remplacements_effectues.csv",
            mime="text/csv"
        )
        st.success("Les IDs ont été anonymisés. Vous pouvez télécharger le fichier modifié.")
