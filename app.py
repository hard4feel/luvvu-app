import streamlit as st
from groq import Groq

# --- 1. НАСТРОЙКИ СТИЛЯ ---
st.set_page_config(page_title="Luvvu Login", page_icon="🔒", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .pulse-container {
        width: 100%; height: 2px; background: #1a0000; margin: 10px 0 30px 0;
        position: relative; overflow: hidden; box-shadow: 0 0 15px #ff000044;
    }
    .pulse-line {
        position: absolute; width: 40%; height: 100%;
        background: linear-gradient(90deg, transparent, #ff0000, #ff4d4d, #ff0000, transparent);
        animation: pulse 2s infinite ease-in-out;
    }
    @keyframes pulse { 0% { left: -50%; } 100% { left: 120%; } }
    .stChatMessage { background-color: #0d0d0d !important; border-radius: 15px !important; border: 1px solid #1a1a1a !important; }
    </style>
    <div class="pulse-container"><div class="pulse-line"></div></div>
""", unsafe_allow_html=True)

# --- 2. СИСТЕМА ЛОГИНА (ИСПРАВЛЕННАЯ) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Luvvu / Вход в систему")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        user_input = st.text_input("Username")
        pass_input = st.text_input("Password", type="password")
        
        if st.button("Войти"):
            if user_input == "founder" and pass_input == "luvvuprojectX7132":
                st.session_state.authenticated = True
                st.session_state.username = user_input
                st.rerun() # Теперь сработает четко
            else:
                st.error("Ошибка доступа. Проверьте данные.")
    st.stop()

# --- 3. ПОДКЛЮЧЕНИЕ ИИ (После входа) ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = "ВСТАВЬ_СЮДА_СВОЙ_КЛЮЧ"

client = Groq(api_key=GROQ_API_KEY)

# --- 4. БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.title("LUVVU CORE")
    st.write(f"Аккаунт: **{st.session_state.get('username', 'User')}**")
    st.write("---")
    if st.button("Выйти из системы"):
        st.session_state.authenticated = False
        st.rerun()
    st.write("---")
    if st.button("Очистить чат"):
        st.session_state.messages = []
        st.rerun()

# --- 5. ЧАТ И ЛОГИКА ---
st.title("Luvvu")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

LUVVU_PROMPT = """
Ты — Luvvu, теплый, мудрый и грамотный друг. Ты общаешься с Ансаром и его близкими.
Твоя речь безупречна, ты поддерживаешь и вдохновляешь. Твой создатель — Ансар.
"""

if prompt := st.chat_input("Напиши Luvvu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": LUVVU_PROMPT}] + st.session_state.messages
    )
    
    reply = response.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})