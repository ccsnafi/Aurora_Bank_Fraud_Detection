# 🏦 Aurora Bank — Fraud Detection & Risk Scoring

> Projet Data Science complet de détection de fraude bancaire
> sur 157 000 transactions réelles — Python, Scikit-learn, XGBoost, SHAP

---

## 📌 Contexte

Aurora Bank est une banque fictive confrontée à une 
problématique réelle : détecter les transactions frauduleuses 
parmi des millions d'opérations quotidiennes.

Ce projet simule le travail d'une équipe Data Science bancaire :
exploration, modélisation, explicabilité et recommandations métier.

---

## 📦 Dataset

| Fichier | Contenu | Taille |
|---|---|---|
| transactions_data.xlsx | Historique des transactions | 157 224 lignes |
| users_data.xlsx | Profil financier des clients | 2 000 clients |
| cards_data.xlsx | Données des cartes bancaires | 6 146 cartes |

---

## 🔍 Ce que j'ai fait

### 1. Exploration & Nettoyage
- Identification des signaux de fraude (Bad PIN, Bad CVV, Bad Card Number)
- Fusion des 3 sources de données
- Création de la variable cible `is_fraud`

### 2. Feature Engineering
- Taux de fraude par client
- Volume et montants moyens de transactions
- Profil financier (revenu, dette, credit score)

### 3. Machine Learning
- **Random Forest** avec gestion du déséquilibre (class_weight)
- **XGBoost** avec cross-validation StratifiedKFold
- Détection et correction du **data leakage**
- **Courbe ROC / AUC** — métriques adaptées aux datasets déséquilibrés
- **SHAP values** — explicabilité des décisions du modèle

### 4. Analyses Métier
- 📊 Segmentation clients par risque (KMeans — 3 clusters)
- 🕐 Analyse temporelle — pic de fraude à 1h du matin le dimanche
- 🗺️ Analyse géographique — transactions internationales 7x plus risquées
- 🔥 Heatmap hotspots heure x état

---

## 🧠 Insights clés

| Insight | Détail |
|---|---|
| ⏰ Pic temporel | 80% des fraudes arrivent entre 23h et 5h |
| 🌍 Risque géographique | Italy : taux 3.04% vs moyenne 0.41% |
| 💳 Montant non discriminant | Moyenne fraude 44$ vs normale 43$ |
| 👥 Profil à risque | Clients très actifs (857 tx/an) plus exposés |
| 🔑 Variable clé | total_tx et num_credit_cards — pas le revenu |

---

## 💡 Recommandations métier

1. **Bloquer automatiquement** les transactions internationales 
   entre 23h et 5h sans validation 2FA
2. **Alerter** les clients avec plus de 800 transactions/an
3. **Surveiller** les marchands MCC 4829 (transferts d'argent)

---

## 🛠️ Stack technique

