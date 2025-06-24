import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Psicologo di Coppia AI", layout="centered")

# CSS semplice per un look moderno e colorato
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
    }
    .title {
        text-align: center;
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 0.2em;
    }
    .subtitle {
        text-align: center;
        color: #34495e;
        margin-top: 0;
        margin-bottom: 2em;
        font-size: 1.2em;
    }
    textarea {
        border-radius: 8px;
        border: 2px solid #2980b9;
        padding: 10px;
        font-size: 1em;
        width: 100%;
        min-height: 120px;
        resize: vertical;
    }
    .response-box {
        background: #ecf0f1;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        font-size: 1em;
        line-height: 1.4;
        color: #2c3e50;
        white-space: pre-wrap;
    }
    button {
        background-color: #2980b9;
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 8px;
        font-size: 1.1em;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    button:hover {
        background-color: #1c5980;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("🧠 Psicologo di Coppia AI")
st.markdown("Inserisci i messaggi di entrambi i partner per analizzare il conflitto e trovare una soluzione.")

partner1_text = st.text_area("Messaggio Partner 1 (es. tu):")
partner2_text = st.text_area("Messaggio Partner 2 (es. lei/lui):")

if "OPENAI_API_KEY" not in st.secrets:
    st.error("❗ Per favore, inserisci la tua API Key di OpenAI in `st.secrets` come 'OPENAI_API_KEY'")
else:
    if st.button("Analizza e Risolvi 🕊️"):
        if not partner1_text.strip() or not partner2_text.strip():
            st.warning("Inserisci il messaggio di entrambi i partner prima di procedere.")
        else:
            prompt = f"""
Sei un esperto psicologo di coppia.

Leggi i due messaggi seguenti e fornisci:

1. Una breve sintesi imparziale del conflitto, mettendo in evidenza emozioni, punti in comune e divergenze.
2. Consigli pratici e soluzioni per aiutare la coppia a risolvere il problema.
3. Domande riflessive da porre a ciascun partner per migliorare la comunicazione e comprensione reciproca.
4. Far chiedere scusa, e convincere entrambi, di aver sbagliato (se è vero) e far notare in che modo. 

Messaggio Partner 1:
\"\"\"{partner1_text}\"\"\"

Messaggio Partner 2:
\"\"\"{partner2_text}\"\"\"
"""

            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                with st.spinner("L'AI sta elaborando la risposta..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=500,
                        temperature=0.7,
                    )
                answer = response.choices[0].message.content
                st.markdown(f'<div class="response-box">{answer}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Errore durante la chiamata all'API OpenAI: {e}")

