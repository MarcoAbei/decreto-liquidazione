import streamlit as st
from transformers import pipeline

# Inizializza il modello Flan-T5
generator = pipeline("text2text-generation", model="google/flan-t5-small")

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
    
    response = generator(prompt, max_length=512, do_sample=True)
    return response[0]['generated_text'].strip()

# Configura Streamlit
st.title("📝 Baby Matteo")
st.write("genera automaticamente un Decreto di Liquidazione con aura infinita")

# Input utente
numero_decreto = st.text_input("Numero Decreto", "DD-001/2025")
data = st.date_input("Data del Decreto")
beneficiario = st.text_input("Beneficiario", "Nome del beneficiario")
importo = st.number_input("Importo (€)", min_value=0.01, format="%.2f")
motivo = st.text_area("Motivazione della Liquidazione", "Indica il motivo del pagamento")

if st.button("Genera Decreto"):
    decreto_generato = generate_decreto(beneficiario, importo, motivo, numero_decreto, data)
    st.subheader("📜 Decreto Generato")
    st.text_area("", decreto_generato, height=300)
    
    # Opzione per il download
    st.download_button(
        label="🗕️ Scarica Decreto",
        data=decreto_generato,
        file_name=f"Decreto_{numero_decreto}.txt",
        mime="text/plain"
    )

st.write("🚀 Powered by Hugging Face & Streamlit")
