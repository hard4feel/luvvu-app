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

# --- 2. СИСТЕМА ЛОГИНА (АВТОРИЗАЦИЯ) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_login():
    if (st.session_state.get("user_input") == "founder" and 
        st.session_state.get("pass_input") == "luvvuprojectX7132"):
        st.session_state.authenticated = True
        st.success("Доступ разрешен. Синхронизация...")
        st.rerun()
    else:
        if st.session_state.get("user_input"):
            st.error("Ошибка доступа. Проверьте данные.")

if not st.session_state.authenticated:
    st.title("🔒 Luvvu / Вход в систему")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input("Username", key="user_input")
        st.text_input("Password", type="password", key="pass_input")
        st.button("Войти", on_click=check_login)
    st.stop()

# --- 3. ПОДКЛЮЧЕНИЕ ИИ (После успешного входа) ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = "ВСТАВЬ_СЮДА_СВОЙ_КЛЮЧ_ДЛЯ_ЛОКАЛЬНОГО_ТЕСТА"

client = Groq(api_key=GROQ_API_KEY)

# --- 4. БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.title("LUVVU CORE")
    st.write(f"Вы вошли как: **{st.session_state.user_input}**")
    st.write("---")
    if st.button("Выйти из аккаунта"):
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