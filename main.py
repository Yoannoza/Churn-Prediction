from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Charger le modèle initial
model = joblib.load('models/model_v1.joblib')

# Créer l'application FastAPI
app = FastAPI()

#Définir le modèle de données d'entrée
class PredictionRequest(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

# Fonction de prétraitement des données
def preprocess_data(request: PredictionRequest):
    # Convertir les données reçues en un DataFrame
    data = pd.DataFrame([request.dict()])
    
    # Traitement des variables binaires (Yes/No)
    binary_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
    for col in binary_cols:
        data[col] = data[col].map({'Yes': 1, 'No': 0})
    
    # Encodage de 'gender' (Female -> 0, Male -> 1)
    data['gender'] = data['gender'].map({'Female': 0, 'Male': 1})
    
    # Encodage de 'SeniorCitizen' (0 ou 1, déjà sous forme numérique)
    
    # Traitement des variables 'InternetService', 'MultipleLines', 'OnlineSecurity', etc.
    cat_cols = ['InternetService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup', 
                'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
                'Contract', 'PaymentMethod']
    data = pd.get_dummies(data, columns=cat_cols, drop_first=True)
    data = data.astype(int)
    
    expected_columns = joblib.load("models/columns.pkl")

    # Transformer les nouvelles données et garantir que toutes les colonnes sont là
    data = data.reindex(columns=expected_columns, fill_value=0)

    
    # Traiter les valeurs manquantes dans 'TotalCharges' avec la médiane
    if pd.isnull(data['TotalCharges'][0]):
        data['TotalCharges'] = data['TotalCharges'].fillna(data['TotalCharges'].median())
    
    # Mise à l'échelle des données numériques si nécessaire
    scaler = StandardScaler()
    numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    data[numeric_cols] = scaler.fit_transform(data[numeric_cols])
    print(data)
    
    return data

# Fonction pour recharger le modèle automatiquement
def load_model():
    global model
    model = joblib.load('models/model_v1.joblib')
    print("Le modèle a été rechargé.")

# Route pour prédire
@app.post("/predict")
def predict(request: PredictionRequest):
    global model
    # Vérifier si le modèle a été mis à jour
    load_model()  # Charger la dernière version du modèle
    
    # Prétraitement des données
    processed_data = preprocess_data(request)
    
    # Convertir les données traitées en un tableau numpy
    input_data = processed_data.values
    
    # Prédire avec le modèle
    prediction = model.predict(input_data)
    
    # Retourner la prédiction
    return {"prediction": int(prediction[0])}
