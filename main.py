from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(
    title="Aurora Bank — Fraud Detection API",
    description="API de scoring de risque fraude bancaire",
    version="1.0.0"
)

class Transaction(BaseModel):
    client_id: int
    total_tx: float
    montant_moyen: float
    montant_max: float
    credit_score: float
    yearly_income: float
    total_debt: float
    current_age: float
    num_credit_cards: float

@app.get("/")
def home():
    return {
        "message": "Aurora Bank Fraud Detection API",
        "version": "1.0.0",
        "status": "online"
    }

@app.post("/predict")
def predict_fraud(transaction: Transaction):
    # Score basé sur les règles métier
    score = 0.0
    if transaction.total_tx > 800:
        score += 0.3
    if transaction.credit_score < 650:
        score += 0.2
    if transaction.montant_max > 1000:
        score += 0.3
    if transaction.num_credit_cards > 4:
        score += 0.2

    score = min(score, 1.0)
    risk_level = "HIGH" if score > 0.7 else "MEDIUM" if score > 0.4 else "LOW"

    return {
        "client_id": transaction.client_id,
        "fraud_score": round(score, 3),
        "risk_level": risk_level,
        "recommendation": (
            "Bloquer la transaction" if risk_level == "HIGH"
            else "Surveillance renforcée" if risk_level == "MEDIUM"
            else "Transaction normale"
        )
    }

@app.get("/health")
def health():
    return {"status": "online", "model": "Rules-based v1.0"}