import pandas as pd

tables_fusions = [
    "drome_2021.csv",
    "drome_2022.csv",
    "drome_2023.csv",
    "drome_2024.csv",
    "drome_2025.csv",
]  #  Liste des dataframes à fusionner

tables_fusions_dpe = [
    "dpe_existant_26.csv",
    "dpe_neuf_26.csv",
]  #  Liste des dataframes à fusionner pour le DPE

for t in tables_fusions:  # Merge des données du DVF
    dvf = pd.read_csv(
        f"table_dvf/{t}", sep=None, engine="python"
    )  #  Lecture du dataframe
    print(f"Le fichier {t} est en cours d'ajout à l'historique")  #  Message de sécurité

    try:
        historique = pd.read_csv("table_dvf/full_dvf.csv", sep=None, engine="python")
        maj_historique = pd.concat([historique, dvf])
        maj_historique.to_csv("table_dvf/full_dvf.csv", index=False)
    except (
        FileNotFoundError
    ) as e:  # En cas d'absence du fichier / premier lancement de la boucle
        dvf.to_csv(
            "table_dvf/full_dvf.csv", index=False
        )  #  Création de la donnée initiale

print("\n === INFO ====")

print("Fusion des tables DVF réalisées, passage aux tables DPE")

for d in tables_fusions_dpe:  # Merge des données du DPE
    dpe = pd.read_csv(
        f"table_dpe/{d}", sep=None, engine="python"
    )  #  Lecture du dataframe
    print(f"Le fichier {d} est en cours d'ajout à l'historique")  #  Message de sécurité

    try:
        historique_dpe = pd.read_csv(
            "table_dpe/dpe_26.csv", sep=None, engine="python"
        )  # Ouverture de l'historique
        maj_historique_dpe = pd.concat(
            [historique_dpe, dpe]
        )  # Concat historique + actuel
        maj_historique_dpe.to_csv(
            "table_dpe/dpe_26.csv", index=False
        )  # Export de l'historique
    except (
        FileNotFoundError
    ) as e:  # En cas d'absence du fichier / premier lancement de la boucle
        dpe.to_csv(
            "table_dpe/dpe_26.csv", index=False
        )  #  Création de la donnée initiale

print("\n === L'ENSEMBLE DE LA FUSION EST TERMINEE ===")
