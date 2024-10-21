import streamlit as st
import pandas as pd

st.title("Anonymisation des données CSV")
data_file = st.file_uploader("Télécharger le fichier CSV avec les informations personnelles : ", type=["csv"])
correspondance_file = st.file_uploader("Télécharger le fichier CSV de correspondance : ", type=["csv"])

if data_file is not None and correspondance_file is not None:
    data_df = pd.read_csv(data_file)
    correspondance_df = pd.read_csv(correspondance_file)


