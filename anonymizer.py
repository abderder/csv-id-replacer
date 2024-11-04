import streamlit as st
import pandas as pd
import json
import io
import zipfile

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
        with io.BytesIO() as buffer:
            with zipfile.ZipFile(buffer, "w") as zip_file:
                # Ajouter le JSON modifié
                zip_file.writestr("fichier_anonymise.json", data_df)
                # Ajouter le CSV des remplacements
                zip_file.writestr("remplacements_effectues.csv", remplacements_csv)

            # Utiliser le contenu du ZIP pour le téléchargement
            st.download_button(
                label="Télécharger le ZIP contenant les fichiers anonymisés",
                data=buffer.getvalue(),
                file_name="fichiers_anonymises.zip",
                mime="application/zip"
            )
            st.success("Anonymisation terminée et fichiers ZIP prêts au téléchargement.")