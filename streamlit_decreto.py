import streamlit as st
from transformers import pipeline

# Inizializza il modello Flan-T5 Base
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# Funzione per generare il decreto completo
def generate_decreto(beneficiario, importo, motivo, numero_decreto, data):
    prompt = f"""
    Genera un Decreto di Liquidazione completo, comprensivo di premesse e testo del decreto, con i seguenti dettagli:
    
    Beneficiario: {beneficiario}
    Importo: {importo} euro
    Motivo del pagamento: {motivo}
    Numero del Decreto: {numero_decreto}
    Data del Decreto: {data}
    
    Esempio:
    PREMESSO che il decreto legislativo 23 giugno 2011, n. 118, disciplina l'armonizzazione dei sistemi contabili;
    VISTO il contratto stipulato in data 12 gennaio 2024 con il beneficiario;
    CONSIDERATO che il servizio è stato regolarmente eseguito e verificato;
    
    DECRETA
    Articolo 1 - È autorizzato il pagamento dell'importo sopra indicato in favore del beneficiario.
    
    Il decreto deve essere formale, includere riferimenti normativi appropriati e seguire lo stile amministrativo italiano.
    """
    
    response = generator(prompt, max_length=512, do_sample=True)
    return response[0]['generated_text'].strip()

# Configura Streamlit
st.title("📝 Generatore di Decreti di Liquidazione")
st.write("Compila i dettagli richiesti per generare automaticamente un decreto di liquidazione completo.")

# Input utente
beneficiario = st.text_input("Beneficiario", "Mario Rossi")
importo = st.number_input("Importo (euro)", min_value=0.0, format="%0.2f")
motivo = st.text_area("Motivo del pagamento", "Compenso per consulenza tecnica")
numero_decreto = st.text_input("Numero del Decreto", "1234")
data = st.date_input("Data del Decreto")

if st.button("Genera Decreto"):
    decreto_generato = generate_decreto(beneficiario, importo, motivo, numero_decreto, data)
    st.subheader("📜 Decreto Generato")
    st.text_area("", decreto_generato, height=400)
    
    # Opzione per il download
    st.download_button(
        label="🗕️ Scarica Decreto",
        data=decreto_generato,
        file_name="Decreto_Liquidazione.txt",
        mime="text/plain"
    )

st.write("🚀 Powered by Hugging Face & Streamlit")
