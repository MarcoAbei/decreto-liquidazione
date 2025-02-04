import streamlit as st
import openai
import os

# Configura la chiave API di OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_decreto(beneficiario, importo, motivo, numero_decreto, data):
    prompt = f"""
    Genera un Decreto di Liquidazione formale con le seguenti informazioni:
    
    Numero decreto: {numero_decreto}
    Data: {data}
    Beneficiario: {beneficiario}
    Importo: {importo} euro
    Motivo: {motivo}
    
    Il testo deve seguire un linguaggio formale e amministrativo, con una struttura che preveda:
    1️⃣ Premesse con riferimenti normativi appropriati.
    2️⃣ Motivazione della liquidazione.
    3️⃣ Sezione "Decreta" con la disposizione del pagamento.
    """
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sei un assistente esperto nella redazione di atti amministrativi."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Configura Streamlit
st.title("📝 Generatore di Decreti di Liquidazione")
st.write("Compila i campi sottostanti per generare automaticamente un Decreto di Liquidazione conforme agli standard amministrativi.")

# Input utente
numero_decreto = st.text_input("Numero Decreto", "DD-001/2025")
data = st.date_input("Data del Decreto")
beneficiario = st.text_input("Beneficiario", "Nome del beneficiario")
importo = st.number_input("Importo (€)", min_value=0.01, format="%.2f")
motivo = st.text_area("Motivazione della Liquidazione", "Indica il motivo del pagamento")

if st.button("Genera Decreto"):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ Imposta la tua chiave API di OpenAI come variabile d'ambiente (OPENAI_API_KEY).")
    else:
        decreto_generato = generate_decreto(beneficiario, importo, motivo, numero_decreto, data)
        st.subheader("📜 Decreto Generato")
        st.text_area("", decreto_generato, height=300)
        
        # Opzione per il download
        st.download_button(
            label="📅 Scarica Decreto",
            data=decreto_generato,
            file_name=f"Decreto_{numero_decreto}.txt",
            mime="text/plain"
        )

st.write("🚀 Powered by OpenAI & Streamlit")