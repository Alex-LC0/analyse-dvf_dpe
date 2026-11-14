# analyse-dvf-dpe
Analyse des données de Demande de Valeur Foncière (DVF) et de Diagnostic de Performance Energétique (DPE) afin de répondre à la question : 

*Une passoire énergétique se vend-t-elle plus ou moins chère qu’un logement mieux noté dans la Drôme ? Et de combien ?*

## Sommaire

- [Résultats clés](#résultats-clés)
- [Contexte](#contexte)
- [Méthodologie](#méthodologie)
- [Stack technique](#stack-technique)
- [Structure du repo](#structure-du-repo)
- [Lancer le projet](#lancer-le-projet)
- [Limites et pistes futures](#limites-et-pistes-futures)
- [Auteur](#auteur)

## Résultats clés

- Le Diagnostic de Performance Energétique (DPE) possède un impact réel sur le prix du m² médian dans la Drôme, ce qui peut s'expliquer par des négociations plus fortes avant la vente.

- Un appartement de catégorie F possède un prix du m² **42%** plus faible qu'un logement classé A, soit une perte de **1251.3 €** du m²

- Une maison de catégorie F possède un prix du m² **23%** plus faible qu'un logement classé A, soit une perte de **660.50€** du m²

- Dans ce département, les appartements semblent plus impactés par le DPE comparé aux maisons (42% vs. 23%)

- Une passoire énergétique se vend environ 11% moins chère peu importe le type de logement (11.61% vs 11.91%) dans la Drôme

## Contexte

Le Diagnostic de Performance Energétique (DPE) renseigne sur la performance énergétique et climatique d'un logement ou d'un bâtiment, en évaluant sa consommation d'énergie et son impact en termes d'émission de gaz à effet de serre. (*Ministères Transition Ecolologique Aménagement du Territoire Transports Ville et Logement*)

Cette performance s'évalue au travers d'une étiquette allant de A (Meilleure performance possible) à G (Pire performance possible) et doit être réalisée tous les 10 ans à l'initiative du propriétaire du logement, et est  obligatoirement affichée dans la vente d'un bien. Le terme de passoire thermique caractérise les logements aux performances les plus faibles (étiquettes F et G) et nécessitant des rénovations importantes. Ces passoires constituent également une cible prioritaire des politiques publiques de rénovation du parc de logement français.

Le DPE possède une importance informationnelle, en renseignant les consommateurs, mais permet également aux propriétaires d'accéder à des aides financières publiques permettant de rénover les passoires énergétiques.

Ainsi, dans ce contexte, le DPE devrait avoir un effet négatif sur le prix d'un bien immobilier, étant donné qu'un logement mal classé nécessitera des travaux ou engendrera des frais importants pour les futurs propriétaires, ce qui se traduira par des négociations plus intenses dans la phase de vente du bien. 

Cette affirmation semble se vérifier dans des sources et analyses antérieures. Cependant, ces dernières sont réalisées par des organismes de rénovation énergétique, qui ne sont pas toujours neutres vis-à-vis des résultats, afin de motiver les venues de futurs clients.

C'est à cette interrogation que j'ai décidé de répondre dans le cadre de ce projet, afin de vérifier si dans la Drôme, une passoire énergétique se vend moins chère et de combien ?

## Méthodologie

- Collecte des données de Demande de Valeur Foncière et de Diagnostic de Performance Energétique sur les sites du gouvernement.
- Fusion des données séparées en années de collecte
- Nettoyage complet des données collectées : Vérification de la taille du jeu, remplissage des valeurs nulles, suppression des doublons (Perte de 127 355 lignes DVF non conformes)
- Fusion des données de DVF et de DPE sur l'adresse et la date d'établissement (antérieur de maximum de 10 ans)
- Analyse et réponse à la question
- Création d'un rapport Power BI interactif par type de logement. 

## Stack technique

- Python 3
- pandas
- matplotlib
- seaborn
- numpy
- Power BI
- DAX
- Power Query

## Structure du repo

```bash
analyse-dvf-dpe/
├── rapport_bi/                  # Tables CSV crée à la suite de l'analyse et utilisées dans Power BI
│   │   └── *.csv
├── table_dpe/                   # Tables CSV non fusionnées contenant les DPE de 2011 à 2025
│   │   └── *.csv
├── table_dvf/                   # Tables CSV non fusionnées contenant les DVF de 2021 à 2025
│   │   └── *.csv               
├── main.ipynb                   # Jupyter Notebook contenant l'ensemble du code d'analyse du projet
├── functions.py                 # Module contenant l'ensemble des fonctions natives de l'analyse
├── fusion.py                    # Script de fusion des .csv de la table DVF et DPE
├── dpe_dvf.pbix                 # Rapport Power BI du projet
├── .gitignore   
└── README.md
```

## Lancer le projet

### Prérequis

- Python 3.14
- Jupyter Notebook (installé via `requirements.txt`)

### 1. Cloner le dépôt et installer les dépendances

```bash
git clone https://github.com/Alex-LC0/analyse-dvf-dpe.git
cd analyse-dvf-dpe
pip install -r requirements.txt
```

### 2. Fusionner les .csv 

```bash
python fusion.py
```
Ce script nettoie fusionne les tables (stockée dans `/table_dvf` et `/table_dpe`) et les stock dans deux tables distinctes (`full_dvf.csv` et `dpe_26`)

### 3. Lancer l'analyse

```bash
jupyter notebook main.ipynb
```
Le notebook s'appuie sur les fonctions de `functions.py` et produit les fichiers CSV nettoyés dans le dossier `rapport_bi/`.


### 4. Consulter le rapport Power BI

Le rapport est disponible au Power BI desktop (nécessaire pour lancer le rapport) : `dpe_dvf.pbix`

## Limites et pistes futures

Ce projet contient une limite majeure qu'il est important de mentionner. La propreté relative de la table DVF brute a fait perdre plus de 127 355 lignes de données, soit **74.4%** de la base de données. Une partie de cette perte s'explique par la concentration de l'analyse autour des ventes. Cependant, le reste est dû à la présence de valeurs absurdes (supérieures ou inférieures aux prix réels du marché drômois), ou alors à la présence de doublons ou de valeurs nulles. De plus, la fusion entre les données DVF et DPE a causé des pertes, notamment sur le critère de date d'établissement qui devait être antérieur à la date de la vente effective.
Ainsi, la perte de ces données pourrait avoir un impact sur le résultat réel de l'analyse, il faut donc prendre en considération ce chiffre et adopter avec précaution les résultats énoncés précédemment dans ce document et dans le rapport Power BI.

A l'avenir, le projet pourrait être appliqué sur d'autres départements, limitrophes à la Drôme (Ardèche, Loire...) afin de vérifier si les résultats obtenus sont proches ou non. Également, le projet pourrait s'inscrire dans une logique nationale en comparant l'ensemble du marché immobilier français, et d'obtenir avec un large jeu de données un résultat d'autant plus fiable.

## Auteur

Alexis LE CALVEZ