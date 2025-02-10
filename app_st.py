import streamlit as st
import requests

# Définir l'URL de l'API FastAPI (remplace localhost par l'URL de Railway après déploiement)
API_URL = "http://127.0.0.1:8000/predict"

# Configuration de la page
st.set_page_config(page_title="Prédiction Churn Client", layout="centered")

# Titre principal
st.title("🔍 Prédiction de Churn Client")
st.write("Entrez les caractéristiques du client et obtenez une prédiction.")

# Création du formulaire utilisateur
gender = st.selectbox("Genre", ["Male", "Female"])
SeniorCitizen = st.radio("Senior Citizen", [0, 1])
Partner = st.radio("Partenaire", ["Yes", "No"])
Dependents = st.radio("Personnes à charge", ["Yes", "No"])
tenure = st.number_input("Durée d'abonnement (mois)", min_value=0, max_value=100, value=12)
PhoneService = st.radio("Service Téléphonique", ["Yes", "No"])
MultipleLines = st.selectbox("Lignes multiples", ["No phone service", "No", "Yes"])
InternetService = st.selectbox("Service Internet", ["DSL", "Fiber optic", "No"])
OnlineSecurity = st.selectbox("Sécurité en ligne", ["No internet service", "No", "Yes"])
OnlineBackup = st.selectbox("Sauvegarde en ligne", ["No internet service", "No", "Yes"])
DeviceProtection = st.selectbox("Protection des appareils", ["No internet service", "No", "Yes"])
TechSupport = st.selectbox("Support Technique", ["No internet service", "No", "Yes"])
StreamingTV = st.selectbox("Streaming TV", ["No internet service", "No", "Yes"])
StreamingMovies = st.selectbox("Streaming Films", ["No internet service", "No", "Yes"])
Contract = st.selectbox("Type de contrat", ["Month-to-month", "One year", "Two year"])
PaperlessBilling = st.radio("Facturation sans papier", ["Yes", "No"])
PaymentMethod = st.selectbox("Moyen de paiement", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
MonthlyCharges = st.number_input("Frais mensuels (€)", min_value=0.0, max_value=200.0, value=50.0)
TotalCharges = st.number_input("Frais totaux (€)", min_value=0.0, value=500.0)

# Création du dictionnaire des données
input_data = {
    "gender": gender,
    "SeniorCitizen": SeniorCitizen,
    "Partner": Partner,
    "Dependents": Dependents,
    "tenure": tenure,
    "PhoneService": PhoneService,
    "MultipleLines": MultipleLines,
    "InternetService": InternetService,
    "OnlineSecurity": OnlineSecurity,
    "OnlineBackup": OnlineBackup,
    "DeviceProtection": DeviceProtection,
    "TechSupport": TechSupport,
    "StreamingTV": StreamingTV,
    "StreamingMovies": StreamingMovies,
    "Contract": Contract,
    "PaperlessBilling": PaperlessBilling,
    "PaymentMethod": PaymentMethod,
    "MonthlyCharges": MonthlyCharges,
    "TotalCharges": TotalCharges
}

# Bouton de prédiction
if st.button("🔍 Prédire le Churn"):
    with st.spinner("Prédiction en cours... ⏳"):
        try:
            # Envoi de la requête POST à l'API
            response = requests.post(API_URL, json=input_data)
            result = response.json()

            # Affichage du résultat
            churn_prediction = result["prediction"]
            if churn_prediction == 1:
                st.error("❌ Le client risque de résilier son abonnement.")
            else:
                st.success("✅ Le client ne risque pas de résilier son abonnement.")

        except Exception as e:
            st.error(f"Erreur lors de la requête API : {e}")

# Footer
st.markdown("---")
st.markdown("📌 **Développé avec FastAPI & Streamlit**")
