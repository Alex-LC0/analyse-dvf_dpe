"""Outils d'analyse et de visualisation des mutations foncières et des DPE.

Ce module regroupe des fonctions utilitaires pour explorer, contrôler et
représenter des données immobilières croisant les mutations foncières
(ventes de biens) et les diagnostics de performance énergétique (DPE),
appliquées au département de la Drôme.

Il s'organise autour de quatre usages : le contrôle de la qualité des
données, le calcul de statistiques descriptives, la classification des
logements selon leur étiquette DPE et la visualisation des résultats.

Fonctions
---------
Contrôle de la qualité des données :
    data_report(df)
        Rapport de qualité sur les mutations foncières (volumétrie,
        doublons, valeurs manquantes, types des colonnes, modalités de
        ``nature_mutation`` et ``type_local``).
    data_report_dpe(df)
        Rapport de qualité sur les DPE, à partir de la colonne
        ``etiquette_dpe``.
    data_report_dpe_2021(df)
        Variante de ``data_report_dpe`` pour les DPE dont la classe
        énergétique est portée par ``classe_consommation_energie``.

Statistiques descriptives :
    rapport_dataframe(df)
        Description statistique (``describe``) du prix au m² et des
        étiquettes DPE.
    descriptive_stat(df, value, categorie)
        Médiane, écart type, quartiles, extrema d'une variable numérique
        et effectifs par modalité d'une variable catégorielle.

Classification :
    categorie_dpe(df)
        Qualifie un logement de « passoire énergétique » (étiquettes F
        et G) ou de « logement performant », ligne par ligne.

Visualisation :
    visu_resultat(df_1, df_2, value_1, value_2)
        Deux diagrammes en barres superposés du prix médian du m².

Colonnes attendues
------------------
Selon les fonctions, les DataFrames doivent contenir tout ou partie des
colonnes suivantes :

- ``date_mutation`` : date de la mutation ;
- ``valeur_fonciere`` : montant de la vente ;
- ``nature_mutation`` : nature de la mutation ;
- ``type_local`` : type de local vendu ;
- ``prix_mcarre`` : prix au mètre carré ;
- ``date_etablissement_dpe`` : date d'établissement du DPE ;
- ``etiquette_dpe`` : étiquette énergétique du DPE (``"A"`` à ``"G"``) ;
- ``classe_consommation_energie`` : classe de consommation énergétique
  (DPE de 2021).

Dépendances
-----------
- ``pandas`` (importé sous l'alias ``pd``) ;
- ``numpy`` (importé sous l'alias ``np``) ;
- ``matplotlib.pyplot`` (importé sous l'alias ``plt``) ;
- ``seaborn`` (importé sous l'alias ``sns``).

Notes
-----
- Les fonctions de rapport renvoient des dictionnaires dont les clés sont
  des libellés en français destinés à la lecture ; elles ne modifient
  jamais le DataFrame fourni.
- ``visu_resultat`` ne renvoie rien : elle construit la figure
  ``matplotlib`` courante.

Examples
--------
>>> import pandas as pd
>>> df = pd.read_csv("donnees_drome.csv")
>>> rapport = data_report(df)
>>> stats = descriptive_stat(df, "prix_mcarre", "etiquette_dpe")
>>> df["categorie"] = df.apply(categorie_dpe, axis=1)
>>> prix_par_categorie = df.groupby("categorie")["prix_mcarre"].median()
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def data_report(df: pd.DataFrame) -> dict:
    """Génère un rapport de qualité sur un jeu de données de mutations foncières.

    La fonction calcule plusieurs indicateurs de qualité : taille,
    doublons, valeurs manquantes, types de données des colonnes clés et
    modalités des variables catégorielles ``nature_mutation`` et
    ``type_local``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame à analyser. Il doit contenir au minimum les colonnes
        suivantes :

        - ``date_mutation`` : date de la mutation ;
        - ``valeur_fonciere`` : montant de la vente ;
        - ``nature_mutation`` : nature de la mutation ;
        - ``type_local`` : type de local vendu.

    Returns
    -------
    dict
        Dictionnaire contenant les clés suivantes :

        - ``"total_lignes"`` (int) : nombre total de lignes du DataFrame ;
        - ``"Nombre de ligne en duplicat"`` (int) : nombre de lignes
          dupliquées ;
        - ``"Nombre de ligne en NaN : "`` (pd.Series) : nombre de valeurs
          manquantes pour chaque colonne ;
        - ``"Format des dates : "`` (numpy.dtype) : type de données de la
          colonne ``date_mutation`` ;
        - ``"Format des ventes"`` (numpy.dtype) : type de données de la
          colonne ``valeur_fonciere`` ;
        - ``"Liste des variable de mutation"`` (list) : valeurs uniques de
          la colonne ``nature_mutation`` ;
        - ``"Liste des types de locaux en vente"`` (list) : valeurs uniques
          de la colonne ``type_local``.

    Raises
    ------
    KeyError
        Si l'une des colonnes requises (``date_mutation``,
        ``valeur_fonciere``, ``nature_mutation``, ``type_local``) est
        absente du DataFrame.

    Notes
    -----
    Les valeurs manquantes (``NaN``) sont incluses dans les listes de
    valeurs uniques retournées pour ``nature_mutation`` et ``type_local``.

    Examples
    --------
    >>> rapport = data_report(df)
    >>> rapport["total_lignes"]
    1500
    """
    quality_report = {
        "total_lignes": len(df),
        "Nombre de ligne en duplicat": df.duplicated().sum(),
        "Nombre de ligne en NaN : ": df.isnull().sum(),
        "Format des dates : ": df["date_mutation"].dtype,
        "Format des ventes": df["valeur_fonciere"].dtype,
        "Liste des variable de mutation": list(df["nature_mutation"].unique()),
        "Liste des types de locaux en vente": list(df["type_local"].unique()),
    }
    return quality_report


def data_report_dpe(df: pd.DataFrame) -> dict:
    """Génère un rapport de qualité sur un jeu de données de diagnostics de performance énergétique (DPE).

    La fonction calcule plusieurs indicateurs de qualité : volumétrie,
    doublons, valeurs manquantes, type de données de la date
    d'établissement du DPE et modalités de l'étiquette énergétique.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame à analyser. Il doit contenir au minimum les colonnes
        suivantes :

        - ``date_etablissement_dpe`` : date d'établissement du DPE ;
        - ``etiquette_dpe`` : étiquette énergétique du DPE.

    Returns
    -------
    dict
        Dictionnaire contenant les clés suivantes :

        - ``"total_lignes"`` (int) : nombre total de lignes du DataFrame ;
        - ``"Nombre de ligne en duplicat"`` (int) : nombre de lignes
          dupliquées ;
        - ``"Nombre de ligne en NaN : "`` (pd.Series) : nombre de valeurs
          manquantes pour chaque colonne ;
        - ``"Format des dates : "`` (numpy.dtype) : type de données de la
          colonne ``date_etablissement_dpe`` ;
        - ``"Liste des variable de DPE"`` (list) : valeurs uniques de la
          colonne ``etiquette_dpe``.

    Raises
    ------
    KeyError
        Si l'une des colonnes requises (``date_etablissement_dpe``,
        ``etiquette_dpe``) est absente du DataFrame.

    Notes
    -----
    Les valeurs manquantes (``NaN``) sont incluses dans la liste des
    valeurs uniques retournée pour ``etiquette_dpe``.

    Examples
    --------
    >>> rapport = data_report_dpe(df)
    >>> rapport["total_lignes"]
    1500
    """
    quality_report = {
        "total_lignes": len(df),
        "Nombre de ligne en duplicat": df.duplicated().sum(),
        "Nombre de ligne en NaN : ": df.isnull().sum(),
        "Format des dates : ": df["date_etablissement_dpe"].dtype,
        "Liste des variable de DPE": list(df["etiquette_dpe"].unique()),
    }
    return quality_report


def data_report_dpe_2021(df) -> dict:
    """Génère un rapport de qualité sur un jeu de données de diagnostics de performance énergétique (DPE) de la période 2021.

    La fonction calcule plusieurs indicateurs de qualité : volumétrie,
    doublons, valeurs manquantes, type de données de la date
    d'établissement du DPE et modalités de la classe de consommation
    d'énergie.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame à analyser. Il doit contenir au minimum les colonnes
        suivantes :

        - ``date_etablissement_dpe`` : date d'établissement du DPE ;
        - ``classe_consommation_energie`` : classe de consommation
          énergétique du logement.

    Returns
    -------
    dict
        Dictionnaire contenant les clés suivantes :

        - ``"total_lignes"`` (int) : nombre total de lignes du DataFrame ;
        - ``"Nombre de ligne en duplicat"`` (int) : nombre de lignes
          dupliquées ;
        - ``"Nombre de ligne en NaN : "`` (pd.Series) : nombre de valeurs
          manquantes pour chaque colonne ;
        - ``"Format des dates : "`` (numpy.dtype) : type de données de la
          colonne ``date_etablissement_dpe`` ;
        - ``"Liste des variable de DPE"`` (list) : valeurs uniques de la
          colonne ``classe_consommation_energie``.

    Raises
    ------
    KeyError
        Si l'une des colonnes requises (``date_etablissement_dpe``,
        ``classe_consommation_energie``) est absente du DataFrame.

    Notes
    -----
    Les valeurs manquantes (``NaN``) sont incluses dans la liste des
    valeurs uniques retournée pour ``classe_consommation_energie``.

    Cette fonction est la variante de ``data_report_dpe`` adaptée au
    format de données où la classe énergétique est portée par la colonne
    ``classe_consommation_energie`` plutôt que ``etiquette_dpe``.

    Examples
    --------
    >>> rapport = data_report_dpe_2021(df)
    >>> rapport["total_lignes"]
    1500
    """
    quality_report = {
        "total_lignes": len(df),
        "Nombre de ligne en duplicat": df.duplicated().sum(),
        "Nombre de ligne en NaN : ": df.isnull().sum(),
        "Format des dates : ": df["date_etablissement_dpe"].dtype,
        "Liste des variable de DPE": list(df["classe_consommation_energie"].unique()),
    }
    return quality_report


def rapport_dataframe(df):
    """Génère un rapport statistique descriptif sur le prix au m² et les étiquettes DPE.

    La fonction applique la méthode ``describe`` de pandas à la colonne
    du prix au mètre carré (variable numérique) et à la colonne de
    l'étiquette DPE (variable catégorielle).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame à analyser. Il doit contenir au minimum les colonnes
        suivantes :

        - ``prix_mcarre`` : prix au mètre carré ;
        - ``etiquette_dpe`` : étiquette énergétique du DPE.

    Returns
    -------
    dict
        Dictionnaire contenant les clés suivantes :

        - ``"Description pour le prix du m² : "`` (pd.Series) : statistiques
          descriptives de la colonne ``prix_mcarre`` (effectif, moyenne,
          écart-type, minimum, quartiles et maximum) ;
        - ``"Description pour les étiquettes DPE"`` (pd.Series) :
          statistiques descriptives de la colonne ``etiquette_dpe``
          (effectif, nombre de modalités distinctes, modalité la plus
          fréquente et sa fréquence).

    Raises
    ------
    KeyError
        Si l'une des colonnes requises (``prix_mcarre``,
        ``etiquette_dpe``) est absente du DataFrame.

    Notes
    -----
    Le contenu de la description dépend du type de la colonne : pour une
    colonne numérique, ``describe`` renvoie des statistiques de
    distribution ; pour une colonne catégorielle ou de type ``object``,
    elle renvoie des statistiques de fréquence.

    Examples
    --------
    >>> rapport = rapport_dataframe(df)
    >>> rapport["Description pour le prix du m² : "]["mean"]
    3250.75
    """
    rapport_df = {
        "Description pour le prix du m² : ": df["prix_mcarre"].describe(),
        "Description pour les étiquettes DPE": df["etiquette_dpe"].describe(),
    }
    return rapport_df


def descriptive_stat(df, value, categorie):
    """Calcule des statistiques descriptives sur une variable numérique et la répartition d'une variable catégorielle.

    La fonction calcule, pour la colonne numérique ``value``, la médiane,
    l'écart type, les premier et troisième quartiles, le maximum et le
    minimum, ainsi que le nombre d'occurrences de chaque modalité de la
    colonne catégorielle ``categorie``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame à analyser.
    value : str
        Nom de la colonne numérique sur laquelle calculer les statistiques
        (médiane, écart type, quartiles, extrema).
    categorie : str
        Nom de la colonne catégorielle dont on dénombre les occurrences
        de chaque modalité.

    Returns
    -------
    dict
        Dictionnaire dont les clés sont construites à partir des noms de
        colonnes fournis :

        - ``"Médiane {value} : "`` (float) : médiane de ``value`` ;
        - ``"Ecart Type {value}"`` (float) : écart type de ``value`` ;
        - ``"Q1 de {value}"`` (float) : premier quartile (25 %) ;
        - ``"Q3 de {value}"`` (float) : troisième quartile (75 %) ;
        - ``"Valeur maximale de {value}"`` (float) : valeur maximale ;
        - ``"Valeur minimale de {value}"`` (float) : valeur minimale ;
        - ``"Nombre d'occurence de {categorie}"`` (pd.Series) : effectif
          de chaque modalité de ``categorie``, trié par ordre décroissant.

    Raises
    ------
    KeyError
        Si ``value`` ou ``categorie`` n'est pas une colonne du DataFrame.
    TypeError
        Si la colonne ``value`` n'est pas de type numérique.

    Notes
    -----
    - L'écart type est calculé avec ``np.std``, c'est-à-dire l'écart type
      de la population (``ddof=0``), et non l'écart type de l'échantillon
      (``ddof=1``) utilisé par défaut dans ``pandas.Series.std``.
    - La médiane, les quartiles, le minimum et le maximum calculés par pandas ignorent les ``NaN``.
    - ``value_counts`` exclut les valeurs manquantes de ``categorie`` par
      défaut.

    Examples
    --------
    >>> stats = descriptive_stat(df, "prix_mcarre", "etiquette_dpe")
    >>> stats["Q1 de prix_mcarre"]
    2450.0
    """
    stats = {
        f"Médiane {value} : ": df[value].median(),  #  Calcul de la médiane
        f"Ecart Type {value}": np.std(df[value]),  #  Calcul de l'écart type
        f"Q1 de {value}": df[value].quantile(0.25),  #  Calcul du Q1 (25%)
        f"Q3 de {value}": df[value].quantile(0.75),  #  Calcul du Q3 (75%)
        f"Valeur maximale de {value}": df[value].max(),  #  Calcul du maximum
        f"Valeur minimale de {value}": df[value].min(),  #  Calcul du minimum
        f"Nombre d'occurence de {categorie}": df[
            categorie
        ].value_counts(),  #  Caclul du nombre d'occurence de la catégorie
    }
    return stats  #  Obtention du rapport


def categorie_dpe(df):
    """Classe un logement en « passoire énergétique » ou « logement performant » selon son étiquette DPE.

    Un logement est considéré comme une passoire énergétique lorsque son
    étiquette DPE est ``"F"`` ou ``"G"``. Dans tous les autres cas, il est
    qualifié de logement performant.

    Cette fonction est conçue pour être appliquée ligne par ligne, par
    exemple avec ``df.apply(categorie_dpe, axis=1)``.

    Parameters
    ----------
    df : pd.Series
        Ligne d'un DataFrame (et non le DataFrame entier). Elle doit
        contenir la clé ``etiquette_dpe`` : étiquette énergétique du
        logement (``"A"`` à ``"G"``).

    Returns
    -------
    str
        - ``"Passoire energetique"`` si l'étiquette DPE est ``"F"`` ou
          ``"G"`` ;
        - ``"Logement performant"`` dans tous les autres cas.

    Raises
    ------
    KeyError
        Si la clé ``etiquette_dpe`` est absente de la ligne fournie.
    ValueError
        Si un DataFrame entier est passé à la place d'une ligne, car
        l'évaluation de la condition porte alors sur une ``Series`` et non
        sur une valeur unique.

    Notes
    -----
    - Toute étiquette différente de ``"F"`` ou ``"G"`` est classée comme
      « Logement performant », y compris les valeurs manquantes (``NaN``)
      ou inattendues. Un logement dont l'étiquette n'est pas renseignée
      sera donc considéré, à tort, comme performant.
    - La comparaison est sensible à la casse : ``"f"`` ne sera pas reconnu
      comme une passoire énergétique.

    Examples
    --------
    >>> df["categorie"] = df.apply(categorie_dpe, axis=1)
    >>> df["categorie"].iloc[0]
    'Logement performant'
    """
    passoire_thermique = ["F", "G"]
    if df["etiquette_dpe"] in passoire_thermique:
        return "Passoire energetique"
    else:
        return "Logement performant"


def visu_resultat(df_1, df_2, value_1, value_2):
    """Affiche deux diagrammes en barres superposés du prix médian du mètre carré en Drôme.

    La fonction crée une figure contenant deux sous-graphiques verticaux.
    Le premier représente les données de ``df_1`` (en cyan), le second
    celles de ``df_2`` (couleur par défaut de seaborn). Chaque barre est
    annotée de sa valeur et chaque graphique est titré à l'aide de
    ``value_1`` et ``value_2``.

    Parameters
    ----------
    df_1 : pd.DataFrame ou pd.Series
        Données du premier graphique, transmises directement à
        ``seaborn.barplot``. Les valeurs à représenter sont typiquement
        les prix médians du m² par modalité (index = catégories).
    df_2 : pd.DataFrame ou pd.Series
        Données du second graphique, avec la même structure que ``df_1``.
    value_1 : str
        Libellé de la catégorie représentée dans le premier graphique,
        inséré dans son titre (« Prix médian du metre carrée en Drôme
        pour les {value_1} »).
    value_2 : str
        Libellé de la catégorie représentée dans le second graphique,
        inséré dans son titre.

    Returns
    -------
    None
        La fonction ne retourne rien : elle construit la figure
        ``matplotlib`` courante. L'affichage dépend de l'environnement
        (par exemple ``plt.show()`` en dehors d'un notebook).

    Notes
    -----
    - La fonction suppose que ``matplotlib.pyplot`` (``plt``) et
      ``seaborn`` (``sns``) sont importés dans le module.
    - La figure mesure 14 x 10 pouces, avec deux sous-graphiques
      (2 lignes, 1 colonne).
    - Les barres d'erreur sont désactivées (``errorbar=None``).
    - Les étiquettes de valeurs sont affichées avec une taille de police
      de 8 pour le premier graphique et de 7 pour le second.
    - Les données sont transmises à ``seaborn.barplot`` sans argument
      ``x`` ni ``y`` : ce comportement suppose un format de données
      compatible (par exemple une ``Series`` ou un DataFrame « large »).
      Le paramètre ``data`` est passé en premier argument positionnel,
      ce qui nécessite une version récente de seaborn.
    - Le titre mentionne « Drôme » en dur : la fonction n'est donc pas
      réutilisable telle quelle pour un autre département.

    Examples
    --------
    >>> prix_par_etiquette = df.groupby("etiquette_dpe")["prix_mcarre"].median()
    >>> prix_par_type = df.groupby("type_local")["prix_mcarre"].median()
    >>> visu_resultat(prix_par_etiquette, prix_par_type,
    ...               "étiquettes DPE", "types de local")
    """
    plt.figure(figsize=(14, 10))
    plt.subplot(2, 1, 1)
    ax = sns.barplot(df_1, color="cyan", errorbar=None)
    ax.bar_label(ax.containers[0], fontsize=8)
    plt.title(f"Prix médian du metre carrée en Drôme pour les {value_1}")
    plt.tight_layout()
    plt.subplot(2, 1, 2)
    ax = sns.barplot(df_2, errorbar=None)
    ax.bar_label(ax.containers[0], fontsize=7)
    plt.title(f"Prix médian du metre carrée en Drôme pour les {value_2}")
    plt.tight_layout()
