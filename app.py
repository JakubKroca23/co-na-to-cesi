import streamlit as st
import openai
import json
import time

# Konfigurace stránky

st.set_page_config(
page_title=“Co na to Češi”,
page_icon=“🎯”,
layout=“wide”
)

# CSS pro tmavě modré téma a profesionální design

st.markdown(”””

<style>
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #1a2f4f 100%);
    }
    
    .main-title {
        text-align: center;
        color: #ffffff;
        font-size: 3.5em;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
        margin-bottom: 10px;
        font-family: 'Arial Black', sans-serif;
    }
    
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    
    .answer-box {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
        border: 3px solid #3b82f6;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .answer-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.5);
        border-color: #60a5fa;
    }
    
    .answer-number {
        display: inline-block;
        background: #3b82f6;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        font-weight: bold;
        font-size: 1.2em;
        margin-right: 15px;
    }
    
    .answer-text {
        color: #ffffff;
        font-size: 1.3em;
        font-weight: bold;
        display: inline-block;
        vertical-align: middle;
    }
    
    .answer-points {
        float: right;
        background: #fbbf24;
        color: #1a2f4f;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    .hidden {
        background: #334155;
        border-color: #475569;
        color: transparent;
        user-select: none;
    }
    
    .hidden .answer-text,
    .hidden .answer-points {
        visibility: hidden;
    }
    
    .question-box {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 8px 30px rgba(37, 99, 235, 0.4);
    }
    
    .question-text {
        color: white;
        font-size: 2em;
        font-weight: bold;
        margin: 0;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        font-size: 1.2em;
        font-weight: bold;
        padding: 15px 40px;
        border-radius: 30px;
        border: none;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.6);
    }
</style>

“””, unsafe_allow_html=True)

# Inicializace session state

if ‘answers’ not in st.session_state:
st.session_state.answers = []
if ‘revealed’ not in st.session_state:
st.session_state.revealed = [False] * 5
if ‘question’ not in st.session_state:
st.session_state.question = “”

def get_survey_results(question):
“”“Zavolá OpenAI API pro získání výsledků průzkumu”””
try:
# Načtení API klíče ze secrets
api_key = st.secrets[“OPENAI_API_KEY”]
client = openai.OpenAI(api_key=api_key)

```
    prompt = f"""Simuluj průzkum mezi 100 Čechy na otázku: "{question}"
```

Vrať STRIKTNĚ POUZE VALIDNÍ JSON pole s 5 nejčastějšími lidovými odpověďmi.
Formát: [
{{“odpoved”: “text odpovědi”, “body”: číslo}},
…
]

Pravidla:

- Odpovědi musí být typicky české, lidové, vtipné ale realistické
- Body reprezentují počet lidí (celkem 100)
- Seřaď od nejvyšších bodů
- Žádný další text, jen JSON pole”””
  
  ```
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jsi expert na české průzkumy veřejného mínění. Vrať pouze validní JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=500
    )
    
    result_text = response.choices[0].message.content.strip()
    
    # Pokus se parsovat JSON
    answers = json.loads(result_text)
    
    # Validace formátu
    if not isinstance(answers, list) or len(answers) != 5:
        raise ValueError("Nesprávný formát odpovědi")
        
    for answer in answers:
        if not isinstance(answer, dict) or 'odpoved' not in answer or 'body' not in answer:
            raise ValueError("Nesprávná struktura odpovědi")
    
    return answers
  ```
  
  except Exception as e:
  st.error(f”Chyba při komunikaci s API: {str(e)}”)
  return None

def reveal_answer(index):
“”“Odkryje odpověď na daném indexu”””
st.session_state.revealed[index] = True

# Hlavní nadpis

st.markdown(’<h1 class="main-title">🎯 CO NA TO ČEŠI</h1>’, unsafe_allow_html=True)
st.markdown(’<p class="subtitle">Hádej 5 nejčastějších odpovědí z průzkumu mezi 100 Čechy!</p>’, unsafe_allow_html=True)

# Input pro otázku

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
question_input = st.text_input(
“Zadej otázku pro průzkum:”,
placeholder=“Např: Co Češi nejraději dělají o víkendu?”,
label_visibility=“collapsed”
)

```
if st.button("🚀 Spustit průzkum", use_container_width=True):
    if question_input.strip():
        with st.spinner("🔍 Ptáme se 100 Čechů..."):
            results = get_survey_results(question_input)
            if results:
                st.session_state.answers = results
                st.session_state.revealed = [False] * 5
                st.session_state.question = question_input
                st.balloons()
                time.sleep(0.5)
                st.rerun()
    else:
        st.warning("Prosím zadej otázku!")
```

# Zobrazení otázky a odpovědí

if st.session_state.answers:
st.markdown(f’<div class="question-box"><p class="question-text">❓ {st.session_state.question}</p></div>’,
unsafe_allow_html=True)

```
# Zobrazení odpovědí
for i, answer in enumerate(st.session_state.answers):
    if st.session_state.revealed[i]:
        st.markdown(f"""
        <div class="answer-box">
            <span class="answer-number">{i+1}</span>
            <span class="answer-text">{answer['odpoved']}</span>
            <span class="answer-points">{answer['body']} bodů</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="answer-box hidden">
            <span class="answer-number">{i+1}</span>
            <span class="answer-text">Skrytá odpověď</span>
            <span class="answer-points">?</span>
        </div>
        """, unsafe_allow_html=True)

# Tlačítka pro odkrytí
st.markdown("---")
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        if not st.session_state.revealed[i]:
            if st.button(f"Odkrýt #{i+1}", key=f"reveal_{i}", use_container_width=True):
                reveal_answer(i)
                st.rerun()
        else:
            st.button(f"✓ Odkryto", key=f"revealed_{i}", disabled=True, use_container_width=True)

# Tlačítko pro odkrytí všech
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if not all(st.session_state.revealed):
        if st.button("🎉 Odkrýt vše", use_container_width=True):
            st.session_state.revealed = [True] * 5
            st.balloons()
            st.rerun()
```

else:
st.info(“👆 Zadej otázku a spusť průzkum!”)

# Footer

st.markdown(”—”)
st.markdown(
‘<p style="text-align: center; color: #64748b; font-size: 0.9em;">Powered by OpenAI GPT-4o | Made with Streamlit ❤️</p>’,
unsafe_allow_html=True
)
