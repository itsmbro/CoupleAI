import streamlit as st
import openai

# --- Impostazioni pagina e grafica ---
st.set_page_config(
    page_title="Psychologist Couple AI",
    page_icon="❤️‍🩹",
    layout="centered",
    initial_sidebar_state="auto",
)

# CSS custom per grafica colorata e moderna
st.markdown("""
<style>
    .big-font {
        font-size:28px !important;
        font-weight: 700;
        color: #d6336c;
        margin-bottom: 0.3em;
    }
    .partner-box {
        background: linear-gradient(135deg, #ffe3ec 0%, #ffd6e8 100%);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 15px rgba(214, 51, 108, 0.3);
    }
    .response-box {
        background: #f9f9f9;
        border-left: 6px solid #d6336c;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        font-size: 18px;
        line-height: 1.5;
    }
    .footer {
        font-size: 12px;
        color: gray;
        margin-top: 40px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("❤️‍🩹 Psicologo di Coppia AI")

st.markdown("### Inserisci i pensieri di entrambi e lascia che l'AI aiuti a trovare una soluzione.")

# Input messaggi separati
with st.container():
    st.markdown('<div class="partner-box"><h3>Partner 1 (Tu)</h3></div>', unsafe_allow_html=True)
    partner1_text = st.text_area("Scrivi qui cosa senti, pensi o vuoi esprimere", key="p1", height=150)

with st.container():
    st.markdown('<div class="partner-box"><h3>Partner 2 (Lei/Lui)</h3></div>', unsafe_allow_html=True)
    partner2_text = st.text_area("Scrivi qui cosa pensa o prova l'altro partner", key="p2", height=150)

if st.button("🧠 Analizza e Risolvi"):
    if not partner1_text.strip() or not partner2_text.strip():
        st.warning("Per favore, inserisci il messaggio di entrambi i partner.")
    else:
        # Preparazione prompt per OpenAI
        prompt = f"""
Sei un esperto psicologo di coppia. partiamo dal presupposto che il tuo obiettivo è far tornare amore e pace, ed eliminare il problema. 

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

        # OpenAI API call (devi inserire la tua API key)
        openai.api_key = st.secrets.get("OPENAI_API_KEY")  # o metti openai.api_key = "la_tua_chiave"
        try:
            with st.spinner("L'AI sta elaborando..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.7,
                )
            answer = response['choices'][0]['message']['content']
            st.markdown(f'<div class="response-box">{answer.replace("\\n","<br>")}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Errore durante la chiamata all'API OpenAI: {e}")

st.markdown('<div class="footer">Powered by OpenAI GPT-4o-mini & Streamlit</div>', unsafe_allow_html=True)
