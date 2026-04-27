# 🏦 Aurora Bank — Fraud Detection & Risk Scoring

> Projet Data Science complet de détection de fraude bancaire  
> sur 157 000 transactions réelles  
> **Stack :** Python · Pandas · Scikit-learn · XGBoost · SHAP · Plotly · FastAPI

---

## 🎯 Contexte & Problématique

Aurora Bank est une banque confrontée à une problématique réelle et critique : **détecter les transactions frauduleuses** parmi des millions d'opérations quotidiennes.

Le défi principal : le taux de fraude est de seulement **0.41%** ce qui signifie que sur 1000 transactions, seulement 4 sont frauduleuses. Ce déséquilibre extrême rend la détection particulièrement complexe.

Ce projet simule le travail complet d'une équipe Data Science bancaire  de l'exploration des données brutes jusqu'au déploiement d'une API en production.

---

## 📦 Dataset

Le dataset contient 3 sources de données distinctes,comme dans un vrai système bancaire où les données viennent de systèmes différents.

| Fichier | Contenu | Taille |
|---|---|---|
| `transactions_data.xlsx` | Historique complet des opérations bancaires | 157 224 lignes |
| `users_data.xlsx` | Profil financier des clients (revenus, dettes, credit score) | 2 000 clients |
| `cards_data.xlsx` | Informations sur les cartes (type, limite, chip...) | 6 146 cartes |

---

## 🗂️ Structure du Projet

```
Aurora_Bank_Fraud_Detection/
│
├── Aurora_Bank_Fraud_Detection.ipynb  ← Notebook principal
│   ├── 1. Imports & Configuration
│   ├── 2. Chargement des données
│   ├── 3. Exploration & Analyse
│   ├── 4. Création variable fraude
│   ├── 5. Feature Engineering
│   ├── 6. Clustering KMeans
│   ├── 7. Random Forest
│   ├── 8. XGBoost + Courbe ROC
│   ├── 9. Data Leakage + SHAP
│   ├── 10. Isolation Forest
│   ├── 11. Analyse Temporelle
│   ├── 12. Analyse Géographique
│   ├── 13. Hotspots Heure x État
│   ├── 14. Vélocité des transactions
│   ├── 15. Dashboard Plotly interactif
│   └── 16. Guide déploiement FastAPI
│
├── main.py   ← API FastAPI déployable en local
└── README.md ← Ce fichier
```

---

## 🔍 Étapes du Projet

### 1️⃣ Exploration & Nettoyage
Avant de modéliser, on comprend les données.
- Identification des signaux de fraude dans la colonne `errors` (Bad PIN, Bad CVV, Bad Card Number, Bad Expiration...)
- Distribution des montants — **insight clé : la fraude ne se détecte pas sur le montant** (43$ normal vs 44$ frauduleux)
- Fusion des 3 sources de données via `client_id`

### 2️⃣ Feature Engineering
Le modèle ne peut pas analyser 157 000 transactions directement.On résume le comportement de chaque client en indicateurs clés :

| Feature | Description | Pourquoi |
|---|---|---|
| `total_tx` | Nombre total de transactions | Volume d'activité |
| `total_fraud` | Nombre d'incidents détectés | Historique de fraude |
| `taux_fraude` | Ratio fraude/total | Indicateur de risque clé |
| `montant_moyen` | Montant moyen des transactions | Profil de dépenses |
| `montant_max` | Transaction maximale | Détection d'anomalies |

> 💡 Le Feature Engineering est l'étape la plus importante 
> en Data Science. Un bon feature engineering vaut mieux 
> qu'un modèle complexe.

### 3️⃣ Machine Learning Supervisé

**Random Forest**
- 100 arbres de décision qui votent ensemble
- Problème détecté : **overfitting** (AUC = 1.0 sur petit dataset)
- Cause : dataset trop petit (303 clients après fusion)

**XGBoost + Cross-Validation**
- Modèle de boosting — apprend de ses erreurs à chaque itération
- StratifiedKFold (5 folds) — évaluation plus robuste
- **Data Leakage détecté et corrigé** :
  - Problème : `total_fraud` dans les features → le modèle "trichait"
  - Solution : features basées uniquement sur le profil client
  - Résultat : AUC = 0.528 → honnête et réaliste

> ⚠️ Le data leakage est l'erreur la plus courante en ML.
> Un AUC honnête à 0.53 vaut mieux qu'un AUC "triché" à 1.0.

**SHAP Values — Explicabilité**
- Ouvre la boîte noire du modèle
- Variables les plus influentes : `total_tx` et `num_credit_cards`
- Contre-intuitif : le `credit_score` a très peu d'impact
- Obligatoire en banque/assurance (RGPD — droit à l'explication)

### 4️⃣ Machine Learning Non Supervisé

**KMeans Clustering — 3 segments identifiés**

| Cluster | Profil | Taux fraude | Revenu moyen |
|---|---|---|---|
| 0 | Clients modestes, peu actifs | 0.3% | 34 644$ |
| 1 | Clients très actifs | 0.7% | 43 950$ |
| 2 | Clients aisés | 0.4% | 62 337$ |

> 💡 Insight clé : ce sont les clients les plus **actifs** 
> qui sont les plus exposés — pas les plus riches.

**Isolation Forest — Détection d'anomalies**
- Détecte les comportements anormaux SANS labels historiques
- 31 clients anomalies identifiés sur 303
- 26 vrais positifs — anomalies ET réellement risqués
- Très utilisé en production bancaire

### 5️⃣ Analyses Métier

**🕐 Analyse Temporelle**
- Pic de fraude à **1h du matin** — les fraudeurs attaquent 
  quand les gens dorment et les équipes sont réduites
- **Dimanche** = jour le plus risqué

**🗺️ Analyse Géographique**
- **Italy : 3.04%** vs moyenne 0.41% → 7x plus risqué
- Les transactions internationales sont massivement sur-représentées

**🔥 Hotspots Heure x État**
- Heatmap combinant heure et localisation
- Italy la nuit = combinaison la plus dangereuse du portefeuille

**⚡ Vélocité des transactions**
- 0.0 min entre deux transactions = transactions simultanées
- Impossible pour un humain → carte clonée ou bot
- 67 clients avec vélocité suspecte ET fraudes confirmées

### 6️⃣ Dashboard Plotly Interactif
4 graphiques zoomables et filtrables :
- Taux de fraude par heure
- Taux de fraude par jour
- Vélocité vs Fraude
- Segmentation Isolation Forest

---

## 💡 Insights Clés & Recommandations

| Insight | Détail | Recommandation |
|---|---|---|
| ⏰ Pic temporel | Fraude maximale à 1h du matin | Surveillance renforcée 23h-5h |
| 🌍 Risque géographique | Italy : 3.04% vs 0.41% moyenne | 2FA obligatoire hors USA |
| 💳 Montant non discriminant | 43$ normal vs 44$ frauduleux | Ne pas se fier au montant |
| 👥 Profil à risque | Clients très actifs (857 tx/an) | Alertes sur vélocité élevée |
| ⚡ Transactions simultanées | 0.0 min entre 2 tx | Blocage automatique |

---

## 🌐 Déploiement FastAPI

L'API transforme le modèle en service web accessible 
par n'importe quelle application (Power BI, mobile, etc.)

### Installation

```bash
pip install fastapi uvicorn
```

### Lancement

```bash
cd chemin/vers/le/dossier
uvicorn main:app --reload
```

### Endpoints disponibles

| Endpoint | Méthode | Description |
|---|---|---|
| `/` | GET | Vérification que l'API tourne |
| `/predict` | POST | Score de risque en temps réel |
| `/health` | GET | Statut du service |

### Exemple de requête

```json
POST http://127.0.0.1:8000/predict

{
  "client_id": 44,
  "total_tx": 900,
  "montant_moyen": 85.5,
  "montant_max": 1200,
  "credit_score": 620,
  "yearly_income": 45000,
  "total_debt": 12000,
  "current_age": 35,
  "num_credit_cards": 5
}
```

### Réponse obtenue

```json
{
  "client_id": 44,
  "fraud_score": 1.0,
  "risk_level": "HIGH",
  "recommendation": "Bloquer la transaction"
}
```

### Documentation interactive
```
http://127.0.0.1:8000/docs
```
Interface Swagger générée automatiquement testable directement dans le navigateur.

---

## 🔮 Prochaines étapes

- **Déploiement cloud**  Azure App Service ou Renderpour une URL publique accessible par tout le monde
- **Intégration Power BI**  connexion via Power Query pour afficher le fraud_score en temps réel dans un dashboard
- **Séries temporelles**  prédiction de l'évolution du taux de fraude dans le temps
- **Modèle en vraie production**  monitoring du drift,réentraînement automatique
---

## 🛠️ Stack Technique

```
Langage       : Python 3.x
Manipulation  : Pandas · NumPy
ML            : Scikit-learn · XGBoost
Explicabilité : SHAP
Visualisation : Matplotlib · Seaborn · Plotly
API           : FastAPI · Uvicorn
Versioning    : Git · GitHub
Environnement : Google Colab · Anaconda
```

---

## 👩🏾‍💻 Auteure

**Afi Tenuda-Eklou**  
Data Analyst certifiée PL-300 | Data Science & IA  
🔗 [LinkedIn](https://linkedin.com/in/afi-tenuda-eklou)  
🐙 [GitHub](https://github.com/ccsnafi)
